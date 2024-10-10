#!/bin/bash
apt install -y tcl
# Clone repository
CUR=$(pwd)
mkdir -p /benchmarks
cd /benchmarks
wget https://www.sqlite.org/src/tarball/sqlite.tar.gz?r=version-3.42.0
tar -xzf 'sqlite.tar.gz?r=version-3.42.0'
cd sqlite/
CC=clang CXX=clang++ ./configure 
bear make
cd "$CUR"