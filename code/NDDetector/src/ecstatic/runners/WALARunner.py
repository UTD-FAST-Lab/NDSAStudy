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


from typing import List

from src.ecstatic.runners.CommandLineToolRunner import CommandLineToolRunner
from src.ecstatic.util.UtilClasses import BenchmarkRecord


class WALARunner(CommandLineToolRunner):

    def get_timeout_option(self) -> List[str]:
        return f"--timeout {self.timeout*60*1000}".split(" ")

    def get_whole_program(self) -> List[str]:
        # WALA does not need a whole-program mode.
        return []

    def get_input_option(self, benchmark_record: BenchmarkRecord) -> List[str]:
        return f"--jars {benchmark_record.name}" \
               f"{(':'+':'.join(benchmark_record.depends_on)) if len(benchmark_record.depends_on) > 0 else ''}".split(" ")

    def dict_to_config_str(self, config_as_dict: dict[str,str]) -> str:
        config_as_str = "";
        for key in config_as_dict:
            if(config_as_dict[key] == 'true'):
                config_as_str = config_as_str + f"--{key} "
            elif(config_as_dict[key] == 'false'):
                config_as_str = config_as_str; #dumb options that are turned off by not giving them?
            else:
                config_as_str = config_as_str + f"--{key} {config_as_dict[key]} "
        return config_as_str;

    def get_output_option(self, output_file: str) -> List[str]:
        return f"-o {output_file}".split(" ")

    def get_task_option(self, task: str) -> str:
        if task == 'cg':
            pass
        else:
            raise NotImplementedError(f'WALA does not support task {task}.')

    def get_base_command(self) -> List[str]:
        return "java -Xmx15g -jar /WALAInterface/target/WALAInterface-1.0-jar-with-dependencies.jar".split(" ")
