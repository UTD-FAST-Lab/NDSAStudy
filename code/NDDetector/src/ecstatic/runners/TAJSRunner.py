import os.path
from random import randbytes
from typing import List, Dict

from src.ecstatic.runners.CommandLineToolRunner import CommandLineToolRunner
from src.ecstatic.util.UtilClasses import BenchmarkRecord


class TAJSRunner (CommandLineToolRunner):
    def get_timeout_option(self) -> List[str]:
        if self.timeout is None:
            return []
        else:
            return f"-time-limit {self.timeout * 60}".split(" ")

    def get_whole_program(self) -> List[str]:
        # shouldn't be necessary
        return []

    def get_input_option(self, benchmark_record: BenchmarkRecord) -> List[str]:
        return f"{benchmark_record.name}".split()

    def get_output_option(self, output_file: str) -> List[str]:
        # callgraph recieves file path argument
        return f"-callgraph {output_file}".split()
        
    def get_task_option(self, task: str) -> List[str]:
        # might need to add to this
        if task == 'cg':
            return []
        else:
            raise NotImplementedError(f'TAJS does not support task {task}.')

    def dict_to_config_str(self, config_as_dict: Dict[str, str]) -> str:
        """
        We need special handling of TAJS's options, because of unsound options and commands without level value


        Parameters
        ----------
        config_as_dict: The dictionary specifying the configuration.
        Returns
        -------
        The corresponding command-line string.
        """
        #config_as_str = ""
        #for k, v in config_as_dict.items():
        #    k: Option
        #    v: Level
        #    for t in k.tags:
        #        if t.startswith('unsound'):
        #            config_as_str = config_as_str + f"-unsound -{k.name} "
        #rest_of_config = ""
        #for k, v in config_as_dict.items():
        #    if len([t for t in k.tags if t.startswith('unsound')]) == 0:
        #        k: Option
        #        v: Level
        #        if isinstance(v.level_name, int) or \
       #                 v.level_name.lower() not in ['false', 'true']:
        #            rest_of_config += f'-{k.name} {v.level_name} '
        #        elif v.level_name.lower() == 'true':
        #            rest_of_config += f'-{k.name} '
#
        # Compute string for the rest of the options which are not unsound.
        # this part may not work
        #return rest_of_config + config_as_str
        config_as_str = "";
        for key in config_as_dict:
            if key.startswith('isunsound_'):
                #phase option, append like this -p 'phase' 'key':'value'
                #format is "phase_'phase'_'key'" = VALUE
                config_as_str = config_as_str + f"-unsound -{key[key.find('_')+1:]} "
            else:
                if(config_as_dict[key] == 'true'):
                    config_as_str = config_as_str + f"-{key} "
                elif(config_as_dict[key] == 'false'):
                    config_as_str = config_as_str; #dumb options that are turned off by not giving them?
                else:
                    config_as_str = config_as_str + f"-{key} {config_as_dict[key]} "
            
        return config_as_str;

    def get_base_command(self) -> List[str]:
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
        ).split()
        cmd = ["java"]
        if self.kwargs.get("nondex"):
            cmd += nondex
        cmd += ["-jar", "/TAJS/dist/tajs-all.jar"]
        return cmd
        