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
#      GNU General Public Licese for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.


import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple

from src.ecstatic.runners.CommandLineToolRunner import CommandLineToolRunner
from src.ecstatic.util.UtilClasses import BenchmarkRecord, DetectionJob


logger = logging.getLogger(__name__)

class PyCGRunner (CommandLineToolRunner):
    
    def get_timeout_option(self) -> List[str]:
        if self.timeout is None:
            return []
        else:
            return f"timeout {self.timeout * 60}s".split(" ")

    def get_input_option(self, benchmark_record: BenchmarkRecord) -> List[str]:
        if 'micro' in benchmark_record.name:
            parts = benchmark_record.name.split('/')
            package = benchmark_record.name.replace(parts[-1], '').strip('/')
            return f"--package {package} {benchmark_record.name}".split()
        else:
            parts = benchmark_record.name.strip('/').split('/')
            package = '/'.join(parts[0:5])
            print(f"package is {package}")
            filelist = []
            for root, dirs, files in os.walk(package):
                for f in files:
                    if f.endswith('.py'):
                        filelist.append(os.path.join(root, f))
                        print(f"package is {os.path.join(root, f)}")
            return f"--package {package} {' '.join(filelist)}".split()
        
    def get_output_option(self, output_file: str) -> List[str]:
        return f"-o {output_file}".split()
    
    def get_base_command(self) -> List[str]:
        return ["pycg"]
    
    def get_output(self, output_folder: str, job: DetectionJob) -> str:
        config_hash = self.dict_hash(job.configuration)
        if 'micro' in job.target.name:
            parts = job.target.name.split('/')
            package = job.target.name.replace(parts[-1], '').strip('/')
            output_file = os.path.join(output_folder,
                                f'{config_hash}_{os.path.basename(package)}_{os.path.basename(job.target.name)}.raw')
        else:
            parts = job.target.name.strip('/').split('/')
            package = '/'.join(parts[0:5])
            output_file = os.path.join(output_folder,
                                f'{config_hash}_{os.path.basename(package)}.py.raw')
        return output_file

    def try_run_job(self, job: DetectionJob, output_folder: str) -> Tuple[str, str]:
        output_file = self.get_output(output_folder, job)

        logging.info(f'Job configuration is {[(str(k), str(v)) for k, v in job.configuration.items()]}')
        config_hash = self.dict_hash(job.configuration)

        cmd = self.get_timeout_option()
        cmd.extend(self.get_base_command())
        cmd.extend(self.get_input_option(job.target))
        cmd.extend(self.get_output_option(output_file))
        config_as_str = self.dict_to_config_str(job.configuration)
        
        if len(config_as_str) > 0:
            cmd.extend(config_as_str.split(" "))
            print(f"config is {config_as_str}")
        
        logging.info(f"Cmd is {cmd}")
        print(f"Cmd is {cmd}")

        ps = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        if not ps.returncode ==0:
            raise RuntimeError(ps.stdout)

        logger.info(f"Stdout from command {' '.join(cmd)} is {ps.stdout}")



        if not os.path.exists(output_file):
            raise RuntimeError(ps.stdout)
        return output_file, ps.stdout
