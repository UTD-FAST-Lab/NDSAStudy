import os
import shutil
import argparse
from pathlib import Path
from src.ecstatic.readers import ReaderFactory
from src.ecstatic.readers.AbstractReader import AbstractReader


def generate_comparable_results(tool, file, reader):
    match tool.lower():
        case "flowdroid" | "amandroid" :
            return set(reader.import_file(file)) 
        case "soot":
            return reader.import_file(file)
    

def move_nd_files(origin, nondex, file, tool, benchmark, iteration):
    output_path = Path('./results') / 'non_determinism_2' / tool / benchmark
    Path(output_path).mkdir(exist_ok=True, parents=True)
    
    nd_dir_path_t = os.path.join(output_path, file)
        
    if not os.path.exists(nd_dir_path_t):
        os.makedirs(nd_dir_path_t)
    
    nd_file_path_s = os.path.join(f"{origin}/{tool}/{benchmark}", f'iteration0/{file}')
    print(nd_file_path_s)
    if os.path.exists(nd_file_path_s):
        shutil.copyfile(nd_file_path_s, os.path.join(nd_dir_path_t, f'run_0'))
    for campaign_index in range(iteration):
        nd_file_path_s = os.path.join(f"{nondex}/{tool}/{benchmark}", f'iteration{campaign_index}/{file}')
        if os.path.exists(nd_file_path_s):
            shutil.copyfile(nd_file_path_s, os.path.join(nd_dir_path_t, f'run_{campaign_index + 1}'))
        
    files = [f for f in os.listdir(nd_dir_path_t)]
    if len(files) == 0:
        os.rmdir(nd_dir_path_t)
    

def checkResults(origin, nondex, o_not_nondeterminism, task, tool, benchmark, iteration):
    reader = ReaderFactory.get_reader_for_task_and_tool(task, tool)
    
    for file in o_not_nondeterminism:
        
        file_s = f'{origin}/{tool}/{benchmark}/iteration0/{file}'
        if not os.path.exists(file_s):
            print(file_s + " not exist")
            move_nd_files(origin, nondex, file, tool, benchmark, iteration)
        else:
            results_s = generate_comparable_results(tool, file_s, reader)
        
            for campaign_index in range(iteration):
                if not os.path.exists(f'{nondex}/{tool}/{benchmark}/iteration{campaign_index}/{file}'):
                    move_nd_files(origin, nondex, file, tool, benchmark, iteration)
                    break
                else:
                    file_t = f'{nondex}/{tool}/{benchmark}/iteration{campaign_index}/{file}'
                    results_t = generate_comparable_results(tool, file_t, reader)

                    if not results_s == results_t:
                        move_nd_files(origin, nondex, file, tool, benchmark, iteration)
                        break
    
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--origin', type=str, help='origin results path')
    parser.add_argument('--nondex', type=str, help='nondex results path')
    parser.add_argument('tool', type=str, help='tool name')
    parser.add_argument('benchmark', type=str, help='benchmark')
    parser.add_argument('task', type=str, help='task')
    parser.add_argument('iteration', type=int, help='iteration')

    args = parser.parse_args()
    
    origin = args.origin
    nondex = args.nondex
    tool = args.tool
    benchmark = args.benchmark
    task = args.task
    iteration = args.iteration
    
    o_nondeterminism = set()

    if os.path.exists(os.path.join(origin, f"non_determinism/{tool}/{benchmark}")):
        origin_nd_results_dir = os.path.join(origin, f"non_determinism/{tool}/{benchmark}")

        for result in os.listdir(origin_nd_results_dir):
            o_nondeterminism.add(result)
    
    o_not_nondeterminism = set()
    origin_results_dir = os.path.join(origin, f"{tool}/{benchmark}/iteration0")
    
    for result in os.listdir(origin_results_dir):
        if result.endswith(".raw") and result not in o_nondeterminism:
            o_not_nondeterminism.add(result)
    
    print((o_not_nondeterminism))
    checkResults(origin, nondex, o_not_nondeterminism, task, tool, benchmark, iteration)


if __name__ == "__main__":
    main()