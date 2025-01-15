import json 
import subprocess
import time
import os
import csv
import argparse
from pathlib import Path
from typing import List, Tuple
from datetime import datetime
from tqdm import tqdm
import multiprocessing
from multiprocessing.dummy import Pool
from src.ecstatic.util.CGCallSite import CGCallSite
from src.ecstatic.util.CGTarget import CGTarget
import xml.etree.ElementTree as ElementTree
from src.ecstatic.models.Flow import Flow


def diff_pycg(fpath, super_set, common_set, diff_set):
    with open(fpath) as cg:
        single_set = set()
        data = json.load(cg)
        for key in data.keys():
            callsite = CGCallSite(key, '', '')
            for val in data[key]:
                target = CGTarget(val, '')
                single_set.add((callsite, target))
        super_set = super_set | single_set
        if len(common_set) > 0:
            common_set = common_set & single_set
        else:
            common_set = single_set
        diff_set.add(frozenset(single_set))
    return super_set, common_set, diff_set   


def diff_code2flow(fpath, super_set, common_set, diff_set):
    with open(fpath) as cg:
        single_set = set()
        data = json.load(cg)
        graph = data['graph']
        nodes = graph['nodes']
        edges = graph['edges']
            
        for e in edges:
            s = nodes[e['source']]
            callsite = CGCallSite(s['label'], s['name'], '')
            t = nodes[e['target']]
            target = CGTarget(f"{t['label']}{t['name']}", '')
            single_set.add((callsite, target))
        super_set = super_set | single_set
        if len(common_set) > 0:
            common_set = common_set & single_set
        else:
            common_set = single_set
        diff_set.add(frozenset(single_set))
    return super_set, common_set, diff_set   


def diff_flowdroid(args):
    if not os.path.exists(os.path.join(args.path, f"{args.tool}/{args.benchmark}")):
        print(f"No nondeterminism results found for {args.tool} and {args.benchmark}")
        return

    nd_results_path = os.path.join(args.path, f"{args.tool}/{args.benchmark}")
    results = []
    for nd in os.listdir(nd_results_path):
        print(os.path.join(nd_results_path, nd))
        dir = os.path.join(nd_results_path, nd)
        
        super_set = set()
        common_set = set()
        diff_set = set()
        
        for file in os.listdir(dir.strip()):
            fpath = os.path.join(dir.strip(), file)
            single_set = set()
            try:
                root = ElementTree.parse(fpath).getroot()
                for f in root.find("Results").findall("Result"):
                    sink = f.find("Sink")
                    for source in f.find("Sources").findall("Source"):
                        single_set.add(Flow(source, sink))
            except (TypeError, AttributeError):
                print(f"Tried to read file {fpath} and it caused an exception.")
            except ElementTree.ParseError:
                print(f"The xml file {fpath} is not properly closed.")
            
            super_set = super_set | single_set
            if len(common_set) > 0:
                common_set = common_set & single_set
            else:
                common_set = single_set
            diff_set.add(frozenset(single_set))
        
        file_count_threshold = 6 if args.nondex else 5
        if len(os.listdir(dir.strip())) < file_count_threshold:
            common_set = set()
            diff_set.add(frozenset())
            
        print(len(common_set))
        print(len(super_set))
        consistency = (len(common_set) / len(super_set)) if len(super_set) > 0 else 0 
        repetitions = len(diff_set)
            
        elements = os.path.basename(dir).removesuffix('.raw').split('_')
        results.append([elements[0], elements[1], consistency, repetitions])

    header = ['config', 'file', 'consistency', 'repetitions']   
    
    output_path = Path('./results') / 'postprocess'
    Path(output_path).mkdir(exist_ok=True, parents=True) 
    
    output_file = f'{output_path}/{args.tool}_{args.benchmark}.csv' if not args.nondex else f'{output_path}/{args.tool}_{args.benchmark}_nondex.csv'
    
    with open(output_file, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(results)
        
def diff_amandroid(fpath, super_set, common_set, diff_set):
    with open(fpath) as f:
        isFlow = False
        single_set = set()
        lines = f.readlines()
        for line in lines:
            if isFlow:
                if 'Source:' in line:
                    source = line.split(': ', 1)[1]
                elif 'Sink:' in line:
                    sink = line.split(': ', 1)[1]
                    single_set.add((source, sink))
                    isFlow = isFlow == False
            else:
                if 'TaintPath:' in line:
                    isFlow = isFlow == False
        super_set = super_set | single_set
        if len(common_set) > 0:
            common_set = common_set & single_set
        else:
            common_set = single_set
        diff_set.add(frozenset(single_set))
    return super_set, common_set, diff_set   


def diff_infer(fpath, super_set, common_set, diff_set):
    with open(fpath) as f:
        isBug = False
        single_set = set()
        for line in f.readlines():
            if isBug:
                bugItems = line.split(': error: ', 1)
                single_set.add((bugItems[0], bugItems[1]))
                isBug = isBug == False
            else:
                if re.match(r"#\d+", line):
                    isBug = isBug == False
        super_set = super_set | single_set
        if len(common_set) > 0:
            common_set = common_set & single_set
        else:
            common_set = single_set
        diff_set.add(frozenset(single_set))
    return super_set, common_set, diff_set


def diff_doop(fpath, super_set, common_set, diff_set):
    with open(fpath) as f:
        single_set = set()
        for line in f:
            line = line.strip()
            toks = line.split('\t')
            if len(toks) == 4:
                res = (CGCallSite(context=toks[0], clazz=toks[1].split('/')[0].strip("<>"), stmt="/".join(toks[1].split('/')[1:])),
                            CGTarget(context=toks[2], target=toks[3]))
            elif len(toks) == 2:
                res = (CGCallSite(context="", clazz=toks[0].split('/')[0].strip("<>"), stmt="/".join(toks[0].split('/')[1:])),
                            CGTarget(context="", target=toks[1]))
            single_set.add(res)
        super_set = super_set | single_set
        if len(common_set) > 0:
            common_set = common_set & single_set
        else:
            common_set = single_set
        diff_set.add(frozenset(single_set))
    return super_set, common_set, diff_set
        
    
def diff_soot(fpath, super_set, common_set, diff_set):
    with open(fpath) as cg:
        single_set = set()
        data = json.load(cg)
        for source, targets in data.items():
            for target in targets:
                single_set.add((source, target))
        super_set = super_set | single_set
        if len(common_set) > 0:
            common_set = common_set & single_set
        else:
            common_set = single_set
        diff_set.add(frozenset(single_set))
    return super_set, common_set, diff_set


def diff_opal(fpath, super_set, common_set, diff_set):
    with open(fpath, "r") as f:
        single_set = set()
        cg = json.load(f)
        for rm in cg["reachableMethods"]:
            caller = rm["method"]
            cs = CGCallSite(caller["declaringClass"], caller["name"], caller["returnType"])
            # print(f'caller:{caller}')
            for callee in rm["callSites"]:
                for target in callee["targets"]:
                    tar = CGTarget(target["name"], target["declaringClass"])
                    # print(f'callee:{target}')
                    single_set.add((cs, tar))
        super_set = super_set | single_set
        if len(common_set) > 0:
            common_set = common_set & single_set
        else:
            common_set = single_set
        diff_set.add(frozenset(single_set))
    return super_set, common_set, diff_set

        
def diff(args):
    tool, dir = args
    print(dir)
    res = []
    super_set = set()
    common_set = set()
    diff_set = set() 
    
    for file in os.listdir(dir.strip()):
        fpath = os.path.join(dir.strip(), file)

        if tool == "soot":
            super_set, common_set, diff_set = diff_soot(fpath, super_set, common_set, diff_set)
        elif tool == "doop":
            super_set, common_set, diff_set = diff_doop(fpath, super_set, common_set, diff_set)
        elif tool == "infer":
            super_set, common_set, diff_set = diff_infer(fpath, super_set, common_set, diff_set)
        elif tool == "amandroid":
            super_set, common_set, diff_set = diff_amandroid(fpath, super_set, common_set, diff_set) 
        elif tool == "code2flow":
            super_set, common_set, diff_set = diff_code2flow(fpath, super_set, common_set, diff_set)
        elif tool == "pycg":
            super_set, common_set, diff_set = diff_pycg(fpath, super_set, common_set, diff_set)
        elif tool == "opal":
            super_set, common_set, diff_set = diff_opal(fpath, super_set, common_set, diff_set)
    
    print(len(common_set))
    print(len(super_set))
    consistency = (len(common_set) / len(super_set)) if len(super_set) > 0 else 0
    repetitions = len(diff_set)
            
    elements = os.path.basename(dir).removesuffix('.raw').split('_')
    res.append([elements[0], elements[1], consistency, repetitions])
    return res

def diff_parallel(args):
    results = []
    campaign_start_time = time.time()
    num_cores = multiprocessing.cpu_count()
    
    nondeterminism_list = []
    nd_results_path = os.path.join(args.path, f"{args.tool}/{args.benchmark}")
    
    for nd in os.listdir(nd_results_path):
        nondeterminism_list.append(os.path.join(nd_results_path, nd))
        
    args_list = [(args.tool, n) for n in nondeterminism_list]
            
    with Pool(num_cores) as p:
        for r in tqdm(p.imap(diff, args_list), total=len(args_list)):
            results.extend(r)
    print(f'Checking finished (time {time.time() - campaign_start_time} seconds)')
    
    header = ['config', 'file', 'consistency', 'repetitions']   
    
    output_path = Path('./results') / 'postprocess'
    Path(output_path).mkdir(exist_ok=True, parents=True) 
    
    output_file = f'{output_path}/{args.tool}_{args.benchmark}.csv' if not args.nondex else f'{output_path}/{args.tool}_{args.benchmark}_nondex.csv'
    
    with open(output_file, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(results)       
        
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--path', type=str, help='results path')
    parser.add_argument('tool', type=str, help='tool name')
    parser.add_argument('benchmark', type=str, help='benchmark')
    parser.add_argument('--nondex', action='store_true')

    args = parser.parse_args()
    
    if args.tool == "flowdroid":
        diff_flowdroid(args)
    else:
        diff_parallel(args)
    

if __name__ == "__main__":
    main()