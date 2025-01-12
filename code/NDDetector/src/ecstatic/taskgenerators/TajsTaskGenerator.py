from src.ecstatic.taskgenerators.AbstractTaskToolGenerator import AbstractTaskToolGenerator
from src.ecstatic.util.UtilClasses import DetectionCampaign, DetectionJob


class TajsTaskGenerator(AbstractTaskToolGenerator):
    def __init__(self):
        a="";
    def read_config_and_generate_jobs(self,benchmark_records):

        configfile="/ECSTATIC/src/resources/configurations/TAJS-2way-covered.csv"
        job_list = []

        header = []
        lines = [];
        
        first=True
        with open(configfile,"r") as readf:
            arrlines = readf.readlines();

    
            for x in arrlines:
                if first:
                    header=x.strip().split(",");
                    first=False
                else:
                    lines.append(x.strip().split(","))

        for configline in lines:
           
            tool_config = dict()
            i=0;
            for x in configline:
                tool_config[header[i]] = x;
                i+=1;
            for x in benchmark_records:
                job_list.append(DetectionJob(tool_config,x))
        retObj = DetectionCampaign(job_list);
        retObj.jobs=job_list;
        return retObj;