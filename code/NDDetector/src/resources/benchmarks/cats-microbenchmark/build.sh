#!/bin/bash

# Clone repository
CUR=$(pwd)
mkdir -p /benchmarks
cd /benchmarks
git clone https://github.com/ICSE2025/CATS-Microbenchmark.git
cd CATS-Microbenchmark

# Build repo
mvn clean compile package

cd "$CUR"