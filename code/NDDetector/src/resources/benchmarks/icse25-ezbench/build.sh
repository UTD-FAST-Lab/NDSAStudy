#!/bin/bash

apt install -y parallel
CURDIR=$(pwd)
mkdir -p /benchmarks
git clone https://github.com/secure-software-engineering/DroidBench.git
cd DroidBench
git checkout develop
find . -type f -name 'JavaThread2.apk' -exec mv {} /benchmarks/ \; -quit
cd $CURDIR