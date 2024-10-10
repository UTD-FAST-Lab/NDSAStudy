from src.ecstatic.util.UtilClasses import DetectionCampaign, DetectionJob
from src.ecstatic.taskgenerators.AbstractTaskToolGenerator import AbstractTaskToolGenerator


class Code2flowTaskGenerator(AbstractTaskToolGenerator):
    def __init__(self):
        a=""
    def read_config_and_generate_jobs(self, benchmark_records):
        configfile="/ECSTATIC/src/resources/configurations/Code2flow-2way-covered.csv"
    
        job_list = []

        header = []
        lines = []
        first=True
        
        benchmark_list = [benchmark_records[0]]
        parts = benchmark_records[0].name.strip('/').split('/')
        package = '/'.join(parts[0:5])
        if 'macro' in benchmark_records[0].name:
            for x in benchmark_records:
                if package not in x.name:
                    benchmark_list.append(x)
                    parts = x.name.strip('/').split('/')
                    package = '/'.join(parts[0:5])
        else:
            benchmark_list = benchmark_records
        
        with open(configfile,"r") as readf:
            arrlines = readf.readlines()
    
            for x in arrlines:
                if first:
                    header=x.strip().split(",")
                    first=False
                else:
                    lines.append(x.strip().split(","))

        for configline in lines:
            tool_config = dict()
            i = 0
            for x in configline:
                tool_config[header[i]] = x
                i+=1
            for x in benchmark_list:
                job_list.append(DetectionJob(tool_config,x))
        retObj = DetectionCampaign(job_list)
        retObj.jobs = job_list
        return retObj