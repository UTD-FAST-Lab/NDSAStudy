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
from src.ecstatic.models.CustomDict import CustomDict

logger = logging.getLogger(__name__)


class SOOTCallGraphReader(AbstractCallGraphReader):
    
    def import_file(self, file: str) -> CustomDict:
        try:
            with open(file, 'r') as f:
                cg_dict = CustomDict(json.load(f))
            return cg_dict
        except AttributeError:
            return CustomDict({})
        except TypeError:
            logger.exception(f"Tried to read file {file} and it caused an exception.")
            return CustomDict({})
