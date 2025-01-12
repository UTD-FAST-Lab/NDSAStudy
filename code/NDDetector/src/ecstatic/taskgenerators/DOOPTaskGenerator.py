from src.ecstatic.util.UtilClasses import DetectionCampaign, DetectionJob
from src.ecstatic.taskgenerators.AbstractTaskToolGenerator import AbstractTaskToolGenerator


class DOOPTaskGenerator(AbstractTaskToolGenerator):
    def __init__(self):
        a="";
    def read_config_and_generate_jobs(self,benchmark_records):
        configfile="/ECSTATIC/src/resources/configurations/DOOP-2way-covered-partial.csv"
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
            #this is one thing we need to turn into dict, and then scroll through benchmarks.
            #header is option, configline content is optionvalue, key - value
            #we handle specific tool things on config later, but this will hold it all
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