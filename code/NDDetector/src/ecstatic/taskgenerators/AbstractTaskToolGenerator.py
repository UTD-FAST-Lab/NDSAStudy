from abc import ABC, abstractmethod

from src.ecstatic.util.UtilClasses import DetectionCampaign, DetectionJob


class AbstractTaskToolGenerator(ABC):
    def __init__(self):
        a="";
    @abstractmethod
    def read_config_and_generate_jobs(self) -> DetectionCampaign:
        return;