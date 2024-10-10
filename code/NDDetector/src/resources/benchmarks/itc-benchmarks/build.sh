#!/bin/bash
apt update
apt install -y automake
CUR=$(pwd)
mkdir -p /benchmarks
cd /benchmarks
git clone https://github.com/regehr/itc-benchmarks.git
cd itc-benchmarks/
aclocal
autoconf
automake --add-missing
CC=clang CXX=clang++ ./configure 
bear make
cd "$CUR"