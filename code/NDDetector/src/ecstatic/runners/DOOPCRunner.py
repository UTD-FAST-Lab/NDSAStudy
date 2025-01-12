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
import shutil
import subprocess
import time
import uuid
from typing import List, Tuple

from src.ecstatic.runners.AbstractCommandLineToolRunner import AbstractCommandLineToolRunner
from src.ecstatic.util.UtilClasses import BenchmarkRecord, DetectionJob

logger = logging.getLogger("DOOPCRunner")


class DOOPCRunner(AbstractCommandLineToolRunner):
    def get_timeout_option(self) -> List[str]:
        return f"-t {self.timeout}".split(" ")

    def get_whole_program(self) -> List[str]:
        return ["--ignore-main-method"]

    def get_input_option(self, benchmark_record: BenchmarkRecord, cache: bool, input_id: str) -> List[str]:
        if cache:
            return f"-i {benchmark_record.name}".split(" ")
        else:
            return f"--input-id {input_id}".split(" ")

    def get_output_option(self, output_file: str) -> List[str]:
        return f"-id {output_file}".split(" ")

    def get_task_option(self, task: str) -> List[str]:
        if task == 'cg':
            return []
        else:
            raise NotImplementedError(f'DOOP does not support task {task}.')

    def get_base_command(self, cache: bool) -> List[str]:
        if cache:
            return ["doop", "--facts-only", "--thorough-fact-gen"]
        else:
            return ["doop"]
        
    def try_run_job(self, job: DetectionJob, output_folder: str) -> Tuple[str, str]:
        iteration = os.path.basename(output_folder)
        os.environ['DOOP_OUT'] = output_folder.removesuffix(f'/{iteration}')
        if iteration == "iteration0":
            cmd = self.get_base_command(True)
        else:
            cmd = self.get_base_command(False)
        
        config_as_str = self.dict_to_config_str(job.configuration)
        cmd.extend(config_as_str.split(" "))
        
        if iteration == "iteration0":
            cmd.extend(self.get_input_option(job.target, True, ""))
        else:
            input_id = f'iteration0_{self.dict_hash(job.configuration)}_{os.path.basename(job.target.name)}.raw'
            cmd.extend(self.get_input_option(job.target, False, input_id))
        
        cmd.extend(self.get_output_option(f'{iteration}_{self.dict_hash(job.configuration)}_{os.path.basename(job.target.name)}.raw'))
        if self.timeout is not None:
            cmd.extend(self.get_timeout_option())
        if self.whole_program:
            cmd.extend(self.get_whole_program())
        logger.info(f"Cmd is {cmd}")
        ps = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        output_file = os.path.join(output_folder,
                            f'{iteration}_{self.dict_hash(job.configuration)}_{os.path.basename(job.target.name)}.raw')

        return output_file, ps.stdout
