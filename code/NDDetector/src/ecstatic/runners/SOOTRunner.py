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
import os.path
from typing import List, Dict
from random import randbytes

from src.ecstatic.runners.CommandLineToolRunner import CommandLineToolRunner
from src.ecstatic.util.UtilClasses import BenchmarkRecord


class SOOTRunner(CommandLineToolRunner):
    def get_whole_program(self) -> List[str]:
        return "-p cg all-reachable:true".split(" ")

    def get_timeout_option(self) -> List[str]:
        # SOOTInterface expects its timeout in milliseconds.
        if self.timeout is None:
            return []
        else:
            return f"--timeout {self.timeout*60*1000}".split(" ")

    def get_input_option(self, benchmark_record: BenchmarkRecord) -> List[str]:
        output = f"--process-dir {benchmark_record.name}"
        if len(benchmark_record.depends_on) > 0:
            output = output + " " + f"--soot-class-path {':'.join(benchmark_record.depends_on)}"
        return output.split(" ")

    def get_output_option(self, output_file: str) -> List[str]:
        return f'--callgraph-output {os.path.abspath(output_file)}'.split(" ")

    def get_task_option(self, task: str) -> str:
        if task == 'cg':
            return "-p cg.spark enabled:true"
        else:
            raise NotImplementedError(f'SOOT does not support task {task}.')

    def dict_to_config_str(self, config_as_dict: Dict[str,str]) -> str:
        """
        We need special handling of SOOT's options, because of phase options.
        Parameters
        ----------
        config_as_dict: The dictionary specifying the configuration.

        Returns
        -------
        The corresponding command-line string.
        """
        config_as_str = "";
        for key in config_as_dict:
            if key.startswith('phase'):
                #phase option, append like this -p 'phase' 'key':'value'
                #format is "phase_'phase'_'key'" = VALUE
                config_as_str = config_as_str + f"-p {key[key.find('_')+1:key.rfind('_')]} {key[key.rfind('_')+1:]}:{config_as_dict[key]} "
            else:
                if(config_as_dict[key] == 'true'):
                    config_as_str = config_as_str + f"--{key} "
                elif(config_as_dict[key] == 'false'):
                    config_as_str = config_as_str; #dumb options that are turned off by not giving them?
                else:
                    config_as_str = config_as_str + f"--{key} {config_as_dict[key]} "

        #config_as_str = ""
        #for k, v in config_as_dict.items():
        #    k: Option
        #    v: Level
        #    for t in k.tags:
        #        if t.startswith('phase'):
        #            config_as_str = config_as_str + f"-p {t.split(' ')[1]} {k.name}:{v.level_name} "
#
        # Compute string for the rest of the options who don't have an associated phase.
        #rest_of_config = super().dict_to_config_str({k: v for k, v in config_as_dict.items() if
        #        
        #                                     len([t for t in k.tags if t.startswith('phase')]) == 0})
        return config_as_str

    def get_base_command(self) -> List[str]:
        # Dynamic due to nondex inclusion
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
            "-DnondexLogging=ALL "
        )
        cmd = "java -Xmx15g "
        # insert nondex config
        cmd += nondex if self.kwargs.get("nondex") else ""
        cmd += "-jar /SootInterface/target/"
        cmd += "SootInterface-1.0-SNAPSHOT-jar-with-dependencies.jar -pp -w -p cg.spark enabled:true"
        return cmd.split(" ")
