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
from typing import List, Tuple


from src.ecstatic.readers.callgraph.AbstractCallGraphReader import AbstractCallGraphReader
from src.ecstatic.util.CGCallSite import CGCallSite
from src.ecstatic.util.CGTarget import CGTarget


logger = logging.getLogger(__name__)
class PyCGCallGraphReader(AbstractCallGraphReader):

    def import_file(self, file):
        callgraph: List[Tuple[Any, Any]] = []
        with open(file) as cg:
            data = json.load(cg)
            for key in data.keys():
                callsite = CGCallSite(key, '', '')
                for val in data[key]:
                    target = CGTarget(val, '')
                    callgraph.append((callsite, target))
        return callgraph
    