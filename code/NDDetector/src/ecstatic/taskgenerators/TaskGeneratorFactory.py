from src.ecstatic.taskgenerators.WalaJSTaskGenerator import WalaJSTaskGenerator
from src.ecstatic.taskgenerators.TajsTaskGenerator import TajsTaskGenerator
from src.ecstatic.taskgenerators.DOOPTaskGenerator import DOOPTaskGenerator
from src.ecstatic.taskgenerators.SOOTTaskGenerator import SOOTTaskGenerator
from src.ecstatic.taskgenerators.WalaTaskGenerator import WalaTaskGenerator
from src.ecstatic.taskgenerators.AbstractTaskToolGenerator import AbstractTaskToolGenerator
from src.ecstatic.taskgenerators.FlowdroidTaskGenerator import FlowdroidTaskGenerator
from src.ecstatic.taskgenerators.DroidSafeTaskGenerator import DroidSafeTaskGenerator
from src.ecstatic.taskgenerators.AmandroidTaskGenerator import AmandroidTaskGenerator
from src.ecstatic.taskgenerators.PyCGTaskGenerator import PyCGTaskGenerator
from src.ecstatic.taskgenerators.Code2flowTaskGenerator import Code2flowTaskGenerator
from src.ecstatic.taskgenerators.InferTaskGenerator import InferTaskGenerator
from src.ecstatic.taskgenerators.OPALTaskGenerator import OPALTaskGenerator


class TaskGeneratorFactory():

    def __init__(self):
        print("made taskgenerator factory");

    def get_task_generator_for_option(self,option:str,benchmark:str) -> AbstractTaskToolGenerator:
        print(option)
        if(option.strip().lower() == "flowdroid"):
            return FlowdroidTaskGenerator();
        elif(option.strip().lower() == "amandroid"):
            return AmandroidTaskGenerator();
        elif(option.strip().lower() == "droidsafe"):
            return DroidSafeTaskGenerator();
        elif(option.strip().lower() == "wala"):
            return WalaTaskGenerator();
        elif(option.strip().lower() == "soot"):
            return SOOTTaskGenerator();
        elif(option.strip().lower() == "doop"):
            return DOOPTaskGenerator();
        elif(option.strip().lower() == "doopc"):
            return DOOPTaskGenerator();
        elif(option.strip().lower() == "tajs"):
            return TajsTaskGenerator();
        elif(option.strip().lower() == "wala-js"):
            return WalaJSTaskGenerator();
        elif(option.strip().lower() == "pycg"):
            return PyCGTaskGenerator();
        elif(option.strip().lower() == "code2flow"):
            return Code2flowTaskGenerator();
        elif(option.strip().lower() == "infer"):
            return InferTaskGenerator(benchmark);
        elif(option.strip().lower() == "opal"):
            return OPALTaskGenerator();
        else:
            print("Tool not supported!");
