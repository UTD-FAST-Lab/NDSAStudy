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


import importlib
import logging
import os
from random import randbytes
import subprocess
import xml.etree.ElementTree as ElementTree
from pathlib import Path
from typing import Dict, Tuple, List

from src.ecstatic.runners.AbstractCommandLineToolRunner import AbstractCommandLineToolRunner
from src.ecstatic.util.UtilClasses import DetectionJob, FinishedDetectionJob, BenchmarkRecord

logger = logging.getLogger(__name__)


def create_shell_file(job: DetectionJob, output_folder: str) -> str:
    """Create a shell script file with the configuration the fuzzer is generating."""
    config_str = FlowDroidRunner.dict_to_config_str(job.configuration)
    hash_value = AbstractCommandLineToolRunner.dict_hash(job.configuration)
    shell_file_dir = os.path.join(output_folder, "shell_files")
    Path(shell_file_dir).mkdir(exist_ok=True)

    shell_file_name = os.path.join(shell_file_dir,
                                   f"{hash_value}.sh")
    if not os.path.exists(shell_file_name):
        logger.debug(f'Creating shell file {shell_file_name}')
        with open(importlib.resources.path("src.resources.tools.flowdroid", "flowdroid.sh"), 'r') as infile:
            content = infile.readlines()

        content = map(lambda r: r.replace('%CONFIG%', config_str), content)
        content = map(lambda r: r.replace('%FLOWDROID_HOME%', "/FlowDroid"), content)
        content = map(lambda r: r.replace('%SOURCE_SINK_LOCATION%',
                                          "/FlowDroid/soot-infoflow-android/SourcesAndSinks.txt"),
                      content)

        with open(shell_file_name, 'w') as f:
            f.writelines(content)

        os.chmod(shell_file_name, 0o777)
    else:
        logger.debug(f'{os.path.basename(shell_file_name)} already exists. Returning.')
    return shell_file_name


class FlowDroidRunner(AbstractCommandLineToolRunner):

    def get_timeout_option(self) -> List[str]:
        if self.timeout is None:
            return []
        else:
            return f"timeout {self.timeout * 60}s".split(" ")

    def get_input_option(self, benchmark_record: BenchmarkRecord) -> List[str]:
        return f"-a {benchmark_record.name}".split(" ")

    def get_output_option(self, output_file: str) -> List[str]:
        return f"-o {output_file}".split(" ")

    def get_base_command(self) -> List[str]:
        # Seed is java int, 4 bytes long
        seed = int.from_bytes(randbytes(4), 'big', signed=True)
        nondex = (
            "-Xbootclasspath/p:/nondex-rt.jar:"
            "/nondex/nondex-common/target/nondex-common.jar "
            "-DnondexFilter='.*' "
            "-DnondexMode=FULL "
            f"-DnondexSeed={seed} "
            "-DnondexStart=0 "
            "-DnondexEnd=9223372036854775807 "
            "-DnondexPrintStack=true "
            "-DnondexDir=\"/nondex\" "
            "-DnondexJarDir=\"/nondex\" "
            "-DnondexExecid=noId "
            "-DnondexLogging=ALL"
        )

        cmd = ["java",]
        if self.kwargs.get("nondex"):
            cmd += nondex.split(" ")
        cmd += [f"-Xmx{os.getenv('MEMORY')}g", "-jar", "/FlowDroid/soot-infoflow-cmd/target/soot-infoflow-cmd-jar-with-dependencies.jar"]
        return cmd

    @staticmethod
    def dict_to_config_str(config_as_dict: dict[str, str]) -> str:
        """Transforms a dictionary to a config string"""
        result = ""
        for k, v in config_as_dict.items():
            if k == 'taintwrapper' and v == 'EASY':  # taintwrapper EASY requires an option
                result += f'--taintwrapper EASY -t /FlowDroid/soot-infoflow/EasyTaintWrapperSource.txt'
            elif v == 'true':
                result += f'--{k} '
            elif v == 'false':
                result = result
            else:
                result += f'--{k} {v} '
            
        return result

    def try_run_job(self, job: DetectionJob, output_folder: str) -> Tuple[str, str]:
        # shell_location: str = create_shell_file(job, output_folder)
        # logger.info(f'Running job with configuration {self.dict_hash(job.configuration)} on apk {job.target.name}')

        # prefix = os.path.basename(shell_location).replace('.sh', '')
        # flowdroid_output = os.path.join(output_folder,
        #                            f"{prefix + '_' + os.path.basename(job.target.name)}.flowdroid.result")
        output_file = self.get_output(output_folder, job)
        
        cmd = self.get_timeout_option()
        cmd.extend(self.get_base_command())
        cmd.extend(self.get_input_option(job.target))
        cmd.extend(["-p", os.getenv('ANDROID_PLATFORMS')])
        cmd.extend(["-s", "/FlowDroid/soot-infoflow-android/SourcesAndSinks.txt"])
        config_as_str = self.dict_to_config_str(job.configuration)
        cmd.extend(config_as_str.split(" "))
        cmd.extend(self.get_output_option(output_file))
        
        ps = subprocess.run(["bash", "-c", " ".join(cmd)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        logger.info(f'Stdout for cmd {" ".join([str(c) for c in cmd])} was {ps.stdout}')
        logger.info(f'Job on configuration {self.dict_hash(job.configuration)} on apk {job.target.name} done.')
        
        return output_file, ps.stdout
    