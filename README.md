# The Artifacts for An Extensive Empirical Study of Nondeterministic Behavior in Static Analysis Tools.

## Table of Contents

- [The Artifacts for An Extensive Empirical Study of Nondeterministic Behavior in Static Analysis Tools](#the-artifacts-for-an-extensive-empirical-study-of-nondeterministic-behavior-in-static-analysis-tools)
  - [Table of Contents](#table-of-contents)
  - [Purpose](#purpose)
  - [Provenance](#provenance)
  - [Data](#data)
    - [RQ1](#rq1)
    - [RQ2](#rq2)
  - [Setup](#setup)
    - [Requirements](#requirements)
    - [Instructions](#instructions)
  - [Usage](#usage)
    - [Basic Usage Example](#basic-usage-example)
    - [How to Read Output](#how-to-read-output)
    - [Replicating Major Paper Results](#replicating-major-paper-results)
    - [Post-processing Results](#post-processing-results)
    

## Purpose

<!--
Purpose: a brief description of what the artifact does.
- Include a list of badge(s) the authors are applying for as well as the reasons
  why the authors believe that the artifact deserves that badge(s).
-->

This artifact contains the code and data for the paper titled ***An Extensive 
Empirical Study of Nondeterministic Behavior in Static Analysis Tools***.

The `code` directory contains the zipped source code of the non-determinism detection 
framework (*NDDetector*) used in RQ2. 

The `data` directory contains files that support the conclusions made in the two research 
questions (RQ1 and RQ2). 

We are applying for the **Available**, **Functional**, and **Reusable** badges.

We believe we deserve the **Available** badge because our artifact is available on Zenodo at https://doi.org/10.5281/zenodo.14630151 (DOI 10.5281/zenodo.14630151) for long-term archiving.

We believe we deserve the **Functional** and **Reusable** badges because our artifact can be executed and used to detect nondeterministic behaviors in static analysis tools. 
Our README.md file gives guidance on how to setup and run the experiments in our paper. 
This artifact also utilizes Docker to facilitate reuse, as recommended in the ICSE 2025 Call for Artifact Submissions.

## Provenance

<!--
Provenance: where the artifact can be obtained, preferably with a link to the
paper’s preprint if publicly available.
-->

The artifact as reported in the original paper is available on Zenodo
(https://doi.org/10.5281/zenodo.14630151). 

A pre-print of the original paper referencing this artifact can be found here:
[An Extensive Empirical Study of Nondeterministic Behavior in Static Analysis Tools](https://annabellam.github.io/docs/An_Extensive_Empirica_Study_of_Nondeterministic_Behavior_in_Static_Analysis_Tools_-_Preprint.pdf).

## Data

<!--
Data (for artifacts which focus on data or include a nontrivial dataset): cover
aspects related to understanding the context, data provenance, ethical and legal
statements (as long as relevant), and storage requirements.
-->

The `data` directory contains files that support the conclusions made in the two research questions (RQ1 and RQ2). 
Inside the `data` directory, there are two sub-directories (`rq1` and `rq2`):

### RQ1

In `rq1/` there are:

`RQ1_FINAL_RESULTS.csv` - Contains 85 distinct results from 7 repositories (SOOT, WALA, DOOP, OPAL, FlowDroid, DroidSafe, Infer) that fix or report nondeterminism, each result is an issue with ID, tool name, linked issues/commits, root cause category, and pattern.

`RQ1_ND_PATTERN_LIST.pdf` - Contains 9 distinct common patterns of nondeterminism, each pattern is described with a pattern ID, description, solution, occurrence in each tool, related results, and a code example.

`raw_data.zip` - Contains the raw commits and issues extracted from 11 repositories (SOOT, DOOP, WALA, OPAL, FlowDroid, DroidSafe, AmanDroid, TAJS, Code2Flow, PyCG, Infer).

`key_words_results.zip` - Contains the results extracted by each keyword (concurrency, concurrent, determinism, deterministic, flakiness, flaky) from the raw data.

### RQ2

In `rq2/` there are two sub-directories (`rq2.1` and `rq2.3`):

In `rq2.1/` there are:

`RQ2_AGGREGATE_DATA.csv` - Contains the result distributions of each combination of target program, configuration hash, and tool as well as the calculated consistency score.

In `rq2.3/` there are:

12 PDF files of each reported issues discussed in RQ2.3, including 3 FLowDorid issues, 2 SOOT issues, 1 issue for DOOP, OPAL, Infer, Amandroid, PyCG and Code2Flow each. Additionally, there is an email from a FlowDroid developer, serving as a response to the FlowDroid-reported-issue-3. We have tried to anonymize all identifiable information such as IDs, names, or links to maintain confidentiality.

## Setup

<!--
Setup (for executable artifacts): provide clear instructions for how to prepare
the artifact for execution. This includes:
- Hardware: performance, storage, and device-type (e.g. GPUs) requirements.
- Software: Docker or VM requirements, or operating system & package
  dependencies if not provided as a container or VM. Providing a Dockerfile or
  image, or at least confirming the tool’s installation in a container is
  strongly encouraged. Any deviation from standard environments needs to be
  reasonably justified.
-->

The `code` directory contains the zipped source code of the non-determinism detection 
framework (*NDDetector*) used in RQ2.

*NDDetector* is a flexible tool that can be used to detect non-deterministic behaviors in configurable static analysis on a variety of benchmarks. 
*NDDetector* can be extended to use alternative analyses, but currently, it can run call graph analyses using WALA, SOOT, DOOP, OPAL, TAJS, PyCG, and Code2Flow, 
taint analysis on Android applications using FlowDroid, AmanDroid, and DroidSafe, as well as vulnerability detection on C programs using Infer.

### Requirements

- Hardware: This artifact works on Windows, Intel/Apple Silicon Macs, and Linux systems running Intel processors. 
- Software:
  - A Python executable of at least version 3.10, including the venv and development packages (`python3.XX-dev` and `python3.XX-venv` on Ubuntu). 
Note that if you installed via `brew` or the Windows installer, your Python should already have these.
  - A C and C++ compiler, e.g., `gcc` and `g++`.
  - GNU `Make`
  - For ARM architectures (e.g., Apple Silicon), you may also require `CMake`.

For example, setting up these dependencies on Ubuntu 22.04 looks like:

```commandline
sudo apt install python3.11 python3.11-dev python3.11-venv g++ gcc make cmake
```
In addition, you must have a working Docker installation (https://docs.docker.com/get-docker/).

### Instructions

To set up the nondeterminism detection framework, we recommend creating a virtual environment. 

To do so, run

`python -m venv <name_of_virtual_environment>`

where `python` points to a Python 3.10 installation. This will create a new folder. If, for example, you named your folder 'venv', then
you can activate it as follows:

`source ./venv/bin/activate`

This will cause `python` to point to the version that you used to create the virtual environment.

In order to install the framework dependencies, from the root directory of the repository, run

`python -m pip install -r requirements.txt`

This will install all of the Python dependencies required. Then, in order to install
the application, run

`python -m pip install -e .`

We require the `-e` to be built in-place. Currently, omitting this option will cause the Dockerfile resolution to fail when we try to build tool-specific images.

This installation will put two executables on your system PATH: `dispatcher`, and `tester`. 
`dispatcher` is the command you run from your host, while `tester` is the command you run from inside the Docker container (under normal usage, a user
will never invoke `tester` themselves, but it can be useful for debugging to skip
container creation.)

Simply run `dispatcher --help` from anywhere in order to see the help doc on how to invoke the detection toolchain.

## Usage

<!--
Usage (for executable artifacts): provide clear instructions for how to
repeat/replicate/reproduce the main results presented in the paper. Include
both:
- A basic usage example or a method to test the installation. For instance, it
  may describe what command to run and what output to expect to confirm that the
  code is installed and operational.
- Detailed commands to replicate the major results from the paper.
-->

***For artifact reviewers:*** These experiments took thousands of hours of machine time to perform. 
We provide smaller experiments to verify the functionality of the artifact in the `Basic Usage Example` section.

### Basic Usage Example

We suggest artifact reviewers use FlowDroid or SOOT, as these tools are relatively faster and more likely to exhibit nondeterministic behaviors compare to other tools, which tend to be slower to build, require significant system memory, or are challenging for capturing nondeterminism.

We have provided small versions of the Droidbench and CATS Microbenchmark under the names `icse25-ezbench` and 
`icse25-ezcats`, respectively. These benchmarks each contain one program which exhibited nondeterministic behaviors:

- `icse25-ezbench` contains *JavaThread2.apk*.
- `icse25-ezcats` contains *TC1.jar*.

For example, to run FlowDroid on `droidbench-small`, run the following command:

```commandline
dispatcher -t flowdroid -b icse25-ezbench --tasks taint -i 5
```

where `-i 5` can be configured to the number of iterations you wish to run. This will create a `results` folder. Details on how to read the contents of this folder are below.

### How to Read Output

By default, the output will be stored at a *results* folder, but the location of the results can be controlled with the `--results-location` option.

We explain the structure of the results through the example above, where we run FlowDroid on the `icse25-ezbench` benchmark.

```commandline
results
|- flowdroid
|  |- icse25-ezbench
|  |  |- iteration0
|  |  |  |- configurations
|  |  |  |  |- 1e9c00f5704518e138859b037784c841
|  |  |  |  |- 3d42058705611ed0e83612b6dff38a35
|  |  |  |  |- ...
|  |  |  |- .1e9c00f5704518e138859b037784c841_JavaThread2-debug.apk.raw.log
|  |  |  |- .1e9c00f5704518e138859b037784c841_JavaThread2-debug.apk.raw.time
|  |  |  |- .3d42058705611ed0e83612b6dff38a35_JavaThread2-debug.apk.raw.log
|  |  |  |- .3d42058705611ed0e83612b6dff38a35_JavaThread2-debug.apk.raw.time
|  |  |  |- ...
|  |  |  |- 1e9c00f5704518e138859b037784c841_JavaThread2-debug.apk.raw
|  |  |  |- 3d42058705611ed0e83612b6dff38a35_JavaThread2-debug.apk.raw
|  |  |  |- ...
|- non-determinism
|  |- flowdroid
|  |  |- icse25-ezbench
|  |  |  |- 7b5480bdb06b2ff39ebfb2bcedd2f657_JavaThread2.apk.raw
|  |  |  |  |- run-0
|  |  |  |  |- run-1
|  |  |  |  |- ...
```

The results of each iteration are stored in their respective folders. For each configuration-program pair, three files are generated, each with a different extension: `.raw`, `.raw.log`, and `.raw.time`. These files correspond to the results produced by the tool, which will be processed by the *ToolReader* implementation, the log for each experiment, and the execution time for each experiment, respectively.

Configurations in the results are represented as hash values. You can see what configuration a hash value represents by looking in the configuration folder. In this example, configuration 1e9c00f5704518e138859b037784c841 corresponds to the configuration `--aplength 10 --cgalgo RTA --nothischainreduction --dataflowsolver CONTEXTFLOWSENSITIVE --aliasflowins --singlejoinpointabstraction --staticmode CONTEXTFLOWSENSITIVE --nostatic --codeelimination PROPAGATECONSTS --implicit ALL --callbackanalyzer FAST --maxcallbackspercomponent 1 --maxcallbacksdepth 1 --enablereflection --pathalgo CONTEXTSENSITIVE --taintwrapper NONE`

The results of non-determinism detection can be found in the `non-determinism` folder. This folder maintains all non-deterministic results across 5 iterations, each batch of results is stored under a folder named as `configration-hash_apk-name.apk.raw`.

In our example, one detected non-determinism is on `JavaThread2.apk` under configuration  `7b5480bdb06b2ff39ebfb2bcedd2f657`.

### Replicating Major Paper Results

The following 24 commands will run experiments for all tool/benchmark combinations using Strategy I, excluding PyCG. 

*Note that as of this writing, PyCG experiments cannot be performed due to errors encountered when running on the Ubuntu system. 
Additionally, PyCG has been archived and is no longer maintained by its development team.*

```commandline
dispatcher -t flowdroid -b droidbench --task taint -j 10 -i 5 --timeout 5
dispatcher -t flowdroid -b fossdroid-all-apks --task taint -j 10 -i 5 --timeout 60

dispatcher -t amandroid -b droidbench --task taint -j 10 -i 5 --timeout 5
dispatcher -t amandroid -b fossdroid-all-apks --task taint -j 10 -i 5 --timeout 60

dispatcher -t droidsafe -b droidbench --task taint -j 10 -i 5 --timeout 60
dispatcher -t droidsafe -b fossdroid-all-apks --task taint -j 10 -i 5 --timeout 120

dispatcher -t soot -b cats-microbenchmark --task cg -j 10 -i 5 --timeout 15
dispatcher -t soot -b dacapo-2006 --task cg -j 10 -i 5 --timeout 120

dispatcher -t wala -b cats-microbenchmark --task cg -j 10 -i 5 --timeout 5
dispatcher -t wala -b dacapo-2006 --task cg -j 10 -i 5 --timeout 60

dispatcher -t doop -b cats-microbenchmark --task cg -j 10 -i 5 --timeout 30
dispatcher -t doop -b dacapo-2006 --task cg -j 10 -i 5 --timeout 120

dispatcher -t opal -b cats-microbenchmark --task cg -j 10 -i 5 --timeout 5
dispatcher -t opal -b dacapo-2006 --task cg -j 10 -i 5 --timeout 30

dispatcher -t infer -b itc-benchmarks --task violation -j 10 -i 5 --timeout 30
dispatcher -t infer -b toybox --task violation -j 10 -i 5 --timeout 30
dispatcher -t infer -b sqlite --task violation -j 10 -i 5 --timeout 30
dispatcher -t infer -b openssl --task violation -j 10 -i 5 --timeout 30

dispatcher -t tajs -b sunspider_test --task cg -j 10 -i 10 --timeout 5
dispatcher -t tajs -b jquery --task cg -j 10 -i 10 --timeout 120

dispatcher -t wala-js -b sunspider_test --task cg -j 10 -i 10 --timeout 5
dispatcher -t wala-js -b jquery --task cg -j 10 -i 10 --timeout 120

dispatcher -t code2flow -b pycg-micro --task cg -j 10 -i 10 --timeout 5
dispatcher -t code2flow -b pycg-macro --task cg -j 10 -i 10 --timeout 5
```

The next 8 commands will run experiments for all compatible analysis tool/benchmark combinations using Strategy II, including Soot, FlowDroid, Amandroid, and TAJS.

```commandline
dispatcher -t flowdroid -b droidbench --task taint -j 10 -i 5 --timeout 5 --results ./results_II --nondex
dispatcher -t flowdroid -b fossdroid-all-apks --task taint -j 10 -i 5 --timeout 60 --results ./results_II --nondex

dispatcher -t amandroid -b droidbench --task taint -j 10 -i 5 --timeout 5 --results ./results_II --nondex
dispatcher -t amandroid -b fossdroid-all-apks --task taint -j 10 -i 5 --timeout 60 --results ./results_II --nondex

dispatcher -t soot -b cats-microbenchmark --task cg -j 10 -i 5 --timeout 15 --results ./results_II --nondex
dispatcher -t soot -b dacapo-2006 --task cg -j 10 -i 5 --timeout 120 --results ./results_II --nondex

dispatcher -t tajs -b sunspider_test --task cg -j 10 -i 10 --timeout 5 --results ./results_II --nondex
dispatcher -t tajs -b jquery --task cg -j 10 -i 10 --timeout 120 --results ./results_II --nondex
```

The results from all the above experiments correspond to those presented in Tables V and VI.

### Post-processing Results

We provide two post-processing scripts to further analyze the results.

First, navigate to the `scripts/analysis` directory.

Use the following command to detect additional nondeterminisms from the Strategy II results:

```
python detector_strategy_2.py --origin <path-to-strategy-I-results-folder> --nondex <path-to-strategy-II-results-folder> <tool> <benchmark> <task> <iteration>
```
This command outputs the detected additional nondeterminisms to the `scripts/analysis/results/non_determinism_2` folder.

We run this script for all compatible analysis tool/benchmark combinations for Strategy II, as described in the previous section.

Next, run the following command to aggregate results for each specified tool-benchmark pair:

```
python post_process.py --path <path-to-non_determinism-folder> <tool> <benchmark>
```

This command generates a CSV file in the `scripts/analysis/results/postprocess` folder, aggregating all results for the specified tool-benchmark pair. It also calculates the percentage of consistent results and the number of distinct results.

We run this script for every tool-benchmark pair, including the additional results detected from the previous command. These results are then consolidated into a single file: `ICSE2025_AGGREGATE_DATA.csv`.

Additionally, we provide a Jupyter notebook, `scripts/notebooks/graphs.ipynb`, to generate figures 3 and 4 for `RQ2.2`. This notebook requires `ICSE2025_AGGREGATE_DATA.csv` as input, containing all results from the CSVs generated by the `post_process.py` script. It is designed to work with the complete dataset, including non-determinism data from all eight tools discussed in the paper.

