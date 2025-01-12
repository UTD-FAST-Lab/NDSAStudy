#!/bin/bash
CURDIR=$(pwd)

mkdir -p benchmarks/
cd benchmarks/
git clone https://github.com/jquery/jquery.git
cd jquery/
git checkout 3.7.0
npm run build

cd $CURDIR
cd $CURDIR
