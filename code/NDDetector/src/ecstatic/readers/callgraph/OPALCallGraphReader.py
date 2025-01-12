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
import json

from src.ecstatic.readers.callgraph.AbstractCallGraphReader import AbstractCallGraphReader
from src.ecstatic.util.CGCallSite import CGCallSite
from src.ecstatic.util.CGTarget import CGTarget


logger = logging.getLogger(__name__)

class OPALCallGraphReader(AbstractCallGraphReader):
    
    def import_file(self, file: str):
        results = []
        with open(file, "r") as f:
            cg = json.load(f)
            for rm in cg["reachableMethods"]:
                caller = rm["method"]
                cs = CGCallSite(caller["declaringClass"], caller["name"], caller["returnType"])
                for callee in rm["callSites"]:
                    for target in callee["targets"]:
                        tar = CGTarget(target["name"], target["declaringClass"])
                        results.append((cs, tar))
        return results
