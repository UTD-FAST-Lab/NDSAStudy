#!/bin/bash
CUR=$(pwd)
mkdir -p /benchmarks
cd /benchmarks
git clone https://github.com/openssl/openssl.git
cd openssl/
CC=clang CXX=clang++ ./Configure 
bear make
cd "$CUR"