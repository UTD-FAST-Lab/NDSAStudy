#  ECSTATIC: Extensible, Customizable STatic Analysis Tester Informed by Configuration
#
#  Copyright (c) 2022.
#
#  This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.


import argparse
import importlib
import json
import logging
import os.path
import pickle
import random
import subprocess
import time
from functools import partial
from multiprocessing.dummy import Pool
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from tqdm import tqdm
import os
import csv
import shutil
from src.ecstatic.taskgenerators.AbstractTaskToolGenerator import AbstractTaskToolGenerator
from src.ecstatic.taskgenerators.TaskGeneratorFactory import TaskGeneratorFactory

from src.ecstatic.readers import ReaderFactory
from src.ecstatic.readers.AbstractReader import AbstractReader
from src.ecstatic.runners import RunnerFactory
from src.ecstatic.runners.AbstractCommandLineToolRunner import AbstractCommandLineToolRunner
from src.ecstatic.util.BenchmarkReader import BenchmarkReader
from src.ecstatic.util.UtilClasses import DetectionCampaign, Benchmark, \
    BenchmarkRecord, FinishedDetectionJob

logger = logging.getLogger(__name__)


class ToolTester:

    def __init__(self,
                 generator,
                 runner: AbstractCommandLineToolRunner,
                 reader: AbstractReader,
                 results_location: str,
                 tool: str,
                 num_processes: int,
                 num_iterations: int,
                 benchmark: Benchmark):
        self.generator = generator
        self.runner: AbstractCommandLineToolRunner = runner
        self.reader: AbstractReader = reader
        self.results_location: str = results_location
        self.tool = tool
        self.num_processes = num_processes
        self.num_iterations = num_iterations
        self.benchmark = benchmark
        
        
    def generate_comparable_results(self, tool, file, reader):
        match tool.lower():
            case "flowdroid" | "tajs" | "droidsafe" | "amandroid" | "sootup" | "pycg" | "code2flow" | "infer" | "opal":
                return set(reader.import_file(file)) 
            case "wala-js" | "wala" | "doop" | "doopc":
                results = []
                with open(file, "r") as f:
                    for line in f:
                        results.append(reader.process_line(line))
                return set(results)
            case "soot":
                return reader.import_file(file)
        
        
    def move_nd_files(self, file, tool, benchmark):
        output_path = Path('/results') / 'non_determinism' / tool / benchmark
        Path(output_path).mkdir(exist_ok=True, parents=True)
        
        if tool == 'infer':
            nd_dir_path_t = os.path.join(output_path, file.removesuffix("/report.txt"))
        elif tool == 'doop':
            nd_dir_path_t = os.path.join(output_path, file.removesuffix("/database/CallGraphEdge.csv"))
        elif tool == 'doopc':
            nd_dir_path_t = os.path.join(output_path, file.removesuffix("/database/CallGraphEdge.csv"))
        else:
            nd_dir_path_t = os.path.join(output_path, file)
            
        if not os.path.exists(nd_dir_path_t):
            os.makedirs(nd_dir_path_t)

        if tool == 'doopc':
            for campaign_index in range(1, self.num_iterations):
                nd_file_path_s = os.path.join(self.results_location, f'iteration{campaign_index}_{file}')
                if os.path.exists(nd_file_path_s):
                    shutil.copyfile(nd_file_path_s, os.path.join(nd_dir_path_t, f'run_{campaign_index-1}'))
        else:
            for campaign_index in range(self.num_iterations):
                nd_file_path_s = os.path.join(self.results_location, f'iteration{campaign_index}/{file}')
                if os.path.exists(nd_file_path_s):
                    shutil.copyfile(nd_file_path_s, os.path.join(nd_dir_path_t, f'run_{campaign_index}'))
            
        files = [f for f in os.listdir(nd_dir_path_t)]
        if len(files) == 0:
            os.rmdir(nd_dir_path_t)
            
    def generate_result_csv(self, results, tool, benchmark):
        header = ['configuration', 'program', 'nondeterminism', 'error']

        output_path = Path('/results') / 'out_csv'
        Path(output_path).mkdir(exist_ok=True, parents=True)
        uuid = datetime.now().strftime('%y%m%dT%H%M%S')
        with open(os.path.join(output_path, f'{tool}_{benchmark}_{uuid}.csv'), 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(results)
            
    def detect_nondeterminism_doopc(self):
        nd_results = []
        locations = str(self.results_location).rsplit('/', 2)
        tool_name = locations[len(locations) - 2]
        benchmark_name = locations[len(locations) - 1]
        allTests = []
        
        end_file = "database/CallGraphEdge.csv"
        
        for file in os.listdir(self.results_location):
            if file.startswith('iteration0_'):
                allTests.append(file.removeprefix("iteration0_"))
        
        for file in allTests:
            nd_result_record = [file.split('_', 2)[1], file.rsplit('_', 1)[-1].removesuffix('.raw')]
            nondeterminism = False
            error = False
            file_s = f'{self.results_location}/iteration1_{file}/{end_file}'
            
            if not os.path.exists(file_s):
                # print(file_s + " not exist")
                error = True
                nondeterminism = True
                self.move_nd_files(f'{file}/{end_file}', tool_name, benchmark_name)
            else:
                results_s = self.generate_comparable_results(tool_name, file_s, self.reader)
                    
                for campaign_index in range(2, self.num_iterations):
                    if not os.path.exists(f'{self.results_location}/iteration{campaign_index}_{file}/{end_file}'):
                        error = True
                        nondeterminism = True
                        self.move_nd_files(f'{file}/{end_file}', tool_name, benchmark_name)
                        break
                    else:
                        file_t = f'{self.results_location}/iteration{campaign_index}_{file}/{end_file}'
                        results_t = self.generate_comparable_results(tool_name, file_t, self.reader)
                        if not results_s == results_t:
                            nondeterminism = True
                            self.move_nd_files(f'{file}/{end_file}', tool_name, benchmark_name)
                            break
            nd_result_record.append(nondeterminism)
            nd_result_record.append(error)
            nd_results.append(nd_result_record)        
        
        # self.generate_result_csv(nd_results, tool_name, benchmark_name)
        
            
    def detect_nondeterminism_dir(self):
        nd_results = []
        locations = str(self.results_location).rsplit('/', 2)
        tool_name = locations[len(locations) - 2]
        benchmark_name = locations[len(locations) - 1]
        allTests = []
        
        end_file = "report.txt" if tool_name == "infer" else "database/CallGraphEdge.csv"
        
        for file in os.listdir(os.path.join(self.results_location, 'iteration0')):
            if file.endswith('.raw.time'):
                allTests.append(file.removesuffix(".time").removeprefix("."))
        
        for file in allTests:
            nd_result_record = [file.split('_', 1)[0], file.rsplit('_', 1)[-1].removesuffix('.raw')]
            nondeterminism = False
            error = False
            file_s = f'{self.results_location}/iteration0/{file}/{end_file}'
            
            if not os.path.exists(file_s):
                # print(file_s + " not exist")
                error = True
                nondeterminism = True
                self.move_nd_files(f'{file}/{end_file}', tool_name, benchmark_name)
            else:
                results_s = self.generate_comparable_results(tool_name, file_s, self.reader)
                    
                for campaign_index in range(1, self.num_iterations):
                    if not os.path.exists(f'{self.results_location}/iteration{campaign_index}/{file}/{end_file}'):
                        error = True
                        nondeterminism = True
                        self.move_nd_files(f'{file}/{end_file}', tool_name, benchmark_name)
                        break
                    else:
                        file_t = f'{self.results_location}/iteration{campaign_index}/{file}/{end_file}'
                        results_t = self.generate_comparable_results(tool_name, file_t, self.reader)
                        if not results_s == results_t:
                            nondeterminism = True
                            self.move_nd_files(f'{file}/{end_file}', tool_name, benchmark_name)
                            break
            nd_result_record.append(nondeterminism)
            nd_result_record.append(error)
            nd_results.append(nd_result_record)        
        
        # self.generate_result_csv(nd_results, tool_name, benchmark_name)
            
    def detect_nondeterminism(self):
        nd_results = []
        locations = str(self.results_location).rsplit('/', 2)
        tool_name = locations[len(locations) - 2]
        benchmark_name = locations[len(locations) - 1]
        allTests = []
        
        for file in os.listdir(os.path.join(self.results_location, 'iteration0')):
            for f_r_type in get_file_types(tool_name):
                if file.endswith(f'.{f_r_type}.raw.time'):
                    allTests.append(file.removesuffix(".time").removeprefix("."))
        
        for file in allTests:
            nd_result_record = [file.split('_', 1)[0], file.rsplit('_', 1)[-1]]
            nondeterminism = False
            error = False
            file_s = f'{self.results_location}/iteration0/{file}'
            
            if not os.path.exists(file_s):
                # print(file_s + " not exist")
                error = True
                nondeterminism = True
                self.move_nd_files(file, tool_name, benchmark_name)
            else:
                results_s = self.generate_comparable_results(tool_name, file_s, self.reader)
                    
                for campaign_index in range(1, self.num_iterations):
                    if not os.path.exists(f'{self.results_location}/iteration{campaign_index}/{file}'):
                        error = True
                        nondeterminism = True
                        self.move_nd_files(file, tool_name, benchmark_name)
                        break
                    else:
                        file_t = f'{self.results_location}/iteration{campaign_index}/{file}'
                        results_t = self.generate_comparable_results(tool_name, file_t, self.reader)
                        if not results_s == results_t:
                            nondeterminism = True
                            self.move_nd_files(file, tool_name, benchmark_name)
                            break
            nd_result_record.append(nondeterminism)
            nd_result_record.append(error)
            nd_results.append(nd_result_record)        
        
        # self.generate_result_csv(nd_results, tool_name, benchmark_name)
              

    def main(self):
        start_time = time.time()
        #timed_out_configs
        timed_out_configs= []
        for campaign_index in range(self.num_iterations):
            campaign = self.generator.read_config_and_generate_jobs(self.benchmark.benchmarks)
            # minus the timed out ones...
            for bad_job in timed_out_configs:
                campaign.jobs.remove(bad_job)
            #for x in campaign.jobs:
                #print(str(x))
            print(f"Running iteration: {campaign_index}.")
            campaign_start_time = time.time()
            # Make campaign folder.
            campaign_folder = os.path.join(self.results_location, f'iteration{campaign_index}')
            Path(campaign_folder).mkdir(exist_ok=True, parents=True)

            # Run all jobs.
            partial_run_job = partial(self.runner.run_job, output_folder=campaign_folder)

            results: List[FinishedDetectionJob] = []
            with Pool(self.num_processes) as p:
                for r in tqdm(p.imap(partial_run_job, campaign.jobs), total=len(campaign.jobs)):
                    results.append(r)
            print(f'Iteration {campaign_index} finished (time {time.time() - campaign_start_time} seconds)')

            minuslist = campaign.jobs.copy()
            #check for all the timedout configs and add to blacklist, all the jobs that didnt finish are bad 
            for fdj in results:
                if fdj != None:
                    if fdj.job in minuslist:
                        minuslist.remove(fdj.job)
            for j in minuslist:
                if j not in timed_out_configs:
                    timed_out_configs.append(j)
        print('Testing done!')
        
        if self.tool == 'infer' or self.tool == 'doop':
            self.detect_nondeterminism_dir()
        elif self.tool == 'doopc':
            self.detect_nondeterminism_doopc()
        else:
            self.detect_nondeterminism()
        

def main():
    p = argparse.ArgumentParser()
    p.add_argument("tool", help="Tool to run.")
    p.add_argument("benchmark", help="Benchmark to download and evaluate on.")
    p.add_argument("-t", "--task", help="Task to run.", default="cg")
    p.add_argument("-j", "--jobs", type=int, default=32,
                   help="Number of parallel jobs to do at once.")
    p.add_argument('--timeout', help='Timeout in minutes', type=int)
    p.add_argument('--verbose', '-v', action='count', default=0)
    p.add_argument('--iterations', '-i', type=int, default=1)
    p.add_argument('--nondex', action='store_true')

    args = p.parse_args()

    if args.verbose > 1:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
    elif args.verbose > 0:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
    else:
        logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    benchmark: Benchmark = build_benchmark(args.benchmark, args.tool)
    logger.info(f'Benchmark is {benchmark}')

    results_location = Path('/results') / args.tool / args.benchmark

    print("tool: "+str(args.tool))

    Path(results_location).mkdir(exist_ok=True, parents=True)
    runner = RunnerFactory.get_runner_for_tool(args.tool, nondex=args.nondex)

    if "dacapo" in args.benchmark.lower():
        runner.whole_program = True
    # Set timeout.
    if args.timeout is not None:
        runner.timeout = args.timeout

    generator = TaskGeneratorFactory().get_task_generator_for_option(args.tool.lower(), args.benchmark.lower())
    reader = ReaderFactory.get_reader_for_task_and_tool(args.task, args.tool.lower())

    t = ToolTester(generator, runner, reader, results_location, args.tool.lower(), args.jobs, args.iterations, benchmark)
    t.main()
    
    

def is_proper_file(tool:str, file:str) -> bool:
    for file_type in get_file_types(tool):
        if file.endswith(file_type):
            return True
    return False

def get_file_types(tool: str):
    match tool.lower():
        case "soot" | "wala" | "doop" | "doopc" | "sootup" | "opal": return ['jar']
        case "wala-js" | "tajs": return ['js']
        case "flowdroid" | "droidsafe" | "amandroid": return ['apk']
        case "pycg" | "code2flow": return ['py']
        case "opt" | "infer": return ['c','cpp']
        
        
def build_benchmark(benchmark: str, tool: str) -> Benchmark:
    # TODO: Check that benchmarks are loaded. If not, load from git.
    if not os.path.exists("/benchmarks"):
        build = importlib.resources.path(f"src.resources.benchmarks.{benchmark}", "build.sh")
        logging.info(f"Building benchmark....")
        subprocess.run(build)
    if os.path.exists(importlib.resources.path(f"src.resources.benchmarks.{benchmark}", "index.json")):
        return BenchmarkReader().read_benchmark(
            importlib.resources.path(f"src.resources.benchmarks.{benchmark}", "index.json"))
    else:
        benchmark_list = []
        for root, dirs, files in os.walk("/benchmarks"):
            benchmark_list.extend([os.path.abspath(os.path.join(root, f)) for f in files if
                                   (is_proper_file(tool,f))])  # TODO more dynamic extensions?
        return Benchmark([BenchmarkRecord(b) for b in benchmark_list])


if __name__ == '__main__':
    main()
