#!/bin/bash
CUR=$(pwd)
mkdir -p /benchmarks
cd /benchmarks
git clone https://github.com/landley/toybox.git
cd toybox/
CC=clang CXX=clang++ ./configure 
bear make
cd "$CUR"