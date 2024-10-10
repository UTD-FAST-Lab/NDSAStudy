from src.ecstatic.util.UtilClasses import DetectionCampaign, DetectionJob
from src.ecstatic.taskgenerators.AbstractTaskToolGenerator import AbstractTaskToolGenerator


class AmandroidTaskGenerator(AbstractTaskToolGenerator):
    def __init__(self):
        a=""

    def create_config_file(self, configs) -> str:
        config_path = '/amandroid/config_'
        with open('/amandroid/config.ini') as f_origin:
            lines = f_origin.readlines()
            f_origin.close()
        
        for key in configs.keys():
            for idx, line in enumerate(lines):
                if key in line:
                    lines[idx] = f'{key} = {configs[key]}'
                    config_path += f'{key}_{configs[key]}'
        
        with open(config_path, 'w') as f_new:
            f_new.writelines(lines)
            f_new.close()
        
        return config_path

    def read_config_and_generate_jobs(self, benchmark_records):
        configfile="/ECSTATIC/src/resources/configurations/Amandroid-2way-covered.csv"
        config_init=['static_init', 'parallel', 'k_context']
    
        job_list = []

        header = []
        lines = []
        first=True
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
            add_config = dict()
            i = 0
            for x in configline:
                if header[i] in config_init:
                    add_config[header[i]] = x
                else:
                    tool_config[header[i]] = x
                i+=1
    
            tool_config['ini'] = self.create_config_file(add_config)
            for x in benchmark_records:
                job_list.append(DetectionJob(tool_config,x))
        retObj = DetectionCampaign(job_list)
        retObj.jobs = job_list
        return retObj