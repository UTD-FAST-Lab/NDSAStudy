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
from typing import Dict, Tuple, List

from src.ecstatic.runners.AbstractCommandLineToolRunner import AbstractCommandLineToolRunner
from src.ecstatic.util.UtilClasses import DetectionJob, FinishedDetectionJob, BenchmarkRecord

logger = logging.getLogger("OPALRunner")


class OPALRunner(AbstractCommandLineToolRunner):
    def get_timeout_option(self) -> List[str]:
        if self.timeout is None:
            return []
        else:
            return f"timeout {self.timeout * 60}s".split(" ")

    def get_input_option(self, benchmark_record: BenchmarkRecord) -> List[str]:
        output = f"{benchmark_record.name}"
        return output.split(" ")

    def get_output_option(self, output_file: str) -> List[str]:
        return f"{output_file}".split(" ")

    @staticmethod
    def dict_to_config_str(config_as_dict: Dict[str, str]) -> str:
        """Transforms a dictionary to a config string"""
        result =""
        for k in config_as_dict:
            result+= f'{config_as_dict[k]} '
        return result.strip()

    def get_base_command(self) -> List[str]:
        return ["java", "-jar", "-Xmx20g", "/OPALInterface/target/OPAL-1.0-SNAPSHOT-jar-with-dependencies.jar"]

    def try_run_job(self, job: DetectionJob, output_folder: str) -> Tuple[str, str]:
        output_file = self.get_output(output_folder, job)
        
        cmd = self.get_timeout_option()
        cmd.extend(self.get_base_command())
        cmd.extend(self.get_input_option(job.target))
        cmd.extend(self.get_output_option(output_file))
        config_as_str = self.dict_to_config_str(job.configuration)
        cmd.extend(config_as_str.split(" "))
        
        ps = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        logger.info(f'Stdout for cmd {" ".join([str(c) for c in cmd])} was {ps.stdout}')
        logger.info(f'Job on configuration {self.dict_hash(job.configuration)} on apk {job.target.name} done.')
        
        return output_file, ps.stdout