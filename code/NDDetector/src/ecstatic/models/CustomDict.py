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


class CustomDict:

    def __init__(self, dict):
        self.dict = dict

    def __eq__(self, other):

        if isinstance(other, CustomDict):
            return self.compare_dicts_ignore_order(self.dict, other.dict)
        return False

    @staticmethod
    def compare_dicts_ignore_order(dict1, dict2):
        # Check if both dictionaries have the same keys
        if set(dict1.keys()) != set(dict2.keys()):
            return False
        # Iterate through keys and compare values (ignoring order for lists)
        for key in dict1.keys():
            if set(dict1[key]) != set(dict2[key]):
                return False
    
        # If all key-value pairs match, dictionaries are equal
        return True
        
    def __hash__(self):

        return hash(frozenset(self.dict))

