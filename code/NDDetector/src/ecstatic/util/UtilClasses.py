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


from dataclasses import dataclass, field
from typing import Dict, Set, List, Any

from frozendict import frozendict

from src.ecstatic.models.Flow import Flow


@dataclass
class BenchmarkRecord:
    name: str
    depends_on: List[str] = field(kw_only=True, default_factory=list)
    sources: List[str] = field(kw_only=True, default_factory=list)
    build_script: str = field(kw_only=True, default=None)
    packages: List[str] = field(kw_only=True, default_factory=list)

    def __hash__(self):
        return hash((self.name, tuple(self.depends_on), tuple(self.sources),
                     self.build_script, tuple(self.packages)))


@dataclass
class Benchmark:
    benchmarks: List[BenchmarkRecord]


class DetectionJob:
    def __init__(self,
                 configuration: Dict[str, str],
                 target: BenchmarkRecord):
        self.configuration = configuration
        self.target = target

    def __eq__(self, other):
        return isinstance(other, DetectionJob) and self.configuration == other.configuration and \
               self.target == other.target

    def as_dict(self) -> Dict[str, Any]:
        return {"configuration": {f"{str(k)}: {str(v)}" for k, v in self.configuration.items()},
                "target": self.target}


@dataclass
class DetectionCampaign:
    jobs: List[DetectionJob]



@dataclass
class FinishedDetectionJob:
    job: DetectionJob
    execution_time: float
    results_location: str


@dataclass
class FlowdroidFinishedDetectionJob(FinishedDetectionJob):
    configuration_location: str
    detected_flows: Dict[str, Set[Flow]]


@dataclass
class FinishedCampaign:
    finished_jobs: List[FinishedDetectionJob]
