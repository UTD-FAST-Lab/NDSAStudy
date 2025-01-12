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


from typing import Tuple
import logging
import os


class Flow:
    """
    Class that represents a flow returned by AQL.
    """
    logger = logging.getLogger(__name__)

    def __init__(self, source, sink):
        self.source = source.get("MethodSourceSinkDefinition")
        self.sink = sink.get("MethodSourceSinkDefinition")

    def get_source_and_sink(self) -> Tuple[str, str]:
        
        return (self.source, self.sink)

    def __str__(self) -> str:
        return f'Flow: {str(self.get_source_and_sink())}'

    def __eq__(self, other):
        """
        Return true if two flows are equal
            
        Criteria:
        1. Same source and sink.
        """

        if not isinstance(other, Flow):
            return False
        else:
            return self.source == other.source and self.sink == other.sink
        
    def __hash__(self):
        sas = self.get_source_and_sink()
        return hash(frozenset(sas))
