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
from src.ecstatic.util.UtilClasses import DetectionJob, FinishedDetectionJob, BenchmarkRecord

logger = logging.getLogger("InferRunner")


class InferRunner(AbstractCommandLineToolRunner):
    def get_timeout_option(self) -> List[str]:
        if self.timeout is None:
            return []
        else:
            return f"timeout {self.timeout * 60}s".split(" ")

    def get_input_option(self, benchmark_record: BenchmarkRecord) -> List[str]:
        return "".split(" ")

    def get_output_option(self, output_file: str) -> List[str]:
        return f"-o {output_file}".split(" ")

    def get_base_command(self) -> List[str]:
        return ["infer", "--compilation-database", "compile_commands.json", "--annotation-reachability", "--bufferoverrun", "--cost", "--loop-hoisting", "--pulse", "--progress-bar"]


    def try_run_job(self, job: DetectionJob, output_folder: str) -> Tuple[str, str]:
        output_file = self.get_output(output_folder, job)
        
        os.chdir(f'/benchmarks/{job.target.name}')
        
        cmd = self.get_timeout_option()
        cmd.extend(self.get_base_command())
        config_as_str = self.dict_to_config_str(job.configuration)
        cmd.extend(config_as_str.split(" "))
        cmd.extend(self.get_output_option(output_file))
        
        ps = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        logger.info(f'Stdout for cmd {" ".join([str(c) for c in cmd])} was {ps.stdout}')
        logger.info(f'Job on configuration {self.dict_hash(job.configuration)} on apk {job.target.name} done.')
        
        return output_file, ps.stdout