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


import logging
import os
import subprocess

from typing import List, Tuple, Dict
from src.ecstatic.runners.CommandLineToolRunner import CommandLineToolRunner
from src.ecstatic.util.UtilClasses import BenchmarkRecord, DetectionJob

logger = logging.getLogger(__name__)

class SOOTUPRunner(CommandLineToolRunner):
               
    def get_timeout_option(self) -> List[str]:
        if self.timeout is None:
            return []
        else:
            return f"timeout {self.timeout * 60}s".split(" ")

    def get_input_option(self, benchmark_record: BenchmarkRecord) -> List[str]:
        return f"-t {benchmark_record.name}".split()
    
    def get_output_option(self, output_file: str) -> List[str]:
        return []
    
    def get_base_command(self) -> List[str]:
        return "java -jar /SootUPInterface/target/sootuprunner-0.0.1.jar".split()
    
    def try_run_job(self, job: DetectionJob, output_folder: str) -> Tuple[str, str]:
        logging.info(f'Job configuration is {[(str(k), str(v)) for k, v in job.configuration.items()]}')
        output_file = f'{output_folder}/{self.dict_hash(job.configuration)}_{os.path.basename(job.target.name)}.raw'
        
        cmd = self.get_timeout_option()
        cmd.extend(self.get_base_command())
        config_as_str = self.dict_to_config_str(job.configuration)
        cmd.extend(config_as_str.replace('--', '-').split(" "))
        cmd.extend(self.get_input_option(job.target))
        
        logging.info(f"Cmd is {cmd}")
        print(f"Cmd is {cmd}")
        
        ps = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        logger.info(f"Stdout from command {' '.join(cmd)} is {ps.stdout}") 

        if not ps.returncode == 0:
            raise RuntimeError(ps.stdout)

        with open(output_file, 'w') as f_new:
            f_new.writelines(ps.stdout)
            f_new.close()

        

        if not os.path.exists(output_file):
            raise RuntimeError(ps.stdout)
        return output_file, ps.stdout
