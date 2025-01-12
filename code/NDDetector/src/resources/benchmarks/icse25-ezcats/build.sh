#!/bin/bash

# Clone repository
CUR=$(pwd)
mkdir -p /benchmarks
cd /benchmarks
git clone https://github.com/amordahl/CATS-Microbenchmark.git
cd CATS-Microbenchmark

# Build repo
cd benchmarks/TypeCasts/TC1
mvn clean package

cd "$CUR"