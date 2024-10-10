#!/bin/bash

#
# CheckMate: A Configuration Tester for Static Analysis
#
# Copyright (c) 2022.
#
# This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

apt install -y parallel
CURDIR=$(pwd)
mkdir -p /benchmarks
git clone https://github.com/secure-software-engineering/DroidBench.git
cd DroidBench
git checkout develop
find . -type f -name 'SharedPreferences1.apk' -exec mv {} /benchmarks/ \; -quit
find . -type f -name 'EventOrdering1.apk' -exec mv {} /benchmarks/ \; -quit
find . -type f -name 'JavaThread2.apk' -exec mv {} /benchmarks/ \; -quit
cd $CURDIR