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
      - [RQ1: Extract Issues and Commits](#rq1:-extract-issues-and-commits)
      - [RQ2](#rq2)
  - [Usage](#usage)
    - [Basic Usage Example](#basic-usage-example)
      - [Detecting Nondeterminism Using Strategy I](#detecting-nondeterminism-using-strategy-i)
      - [How to Read Output](#how-to-read-output)
      - [Detecting Nondeterminism Using Strategy II](#detecting-nondeterminism-using-strategy-ii)
      - [Post-processing Results](#post-processing-results)
    - [Replicating Major Paper Results](#replicating-major-paper-results)
    - [Troubleshooting](#troubleshooting)
    

## Purpose

<!--
Purpose: a brief description of what the artifact does.
- Include a list of badge(s) the authors are applying for as well as the reasons
  why the authors believe that the artifact deserves that badge(s).
-->

This artifact contains the code and data for the paper titled ***An Extensive 
Empirical Study of Nondeterministic Behavior in Static Analysis Tools***.

The `code` directory contains the scripts to extract the issues and commits from each tool's GitHub repository and the source code of the non-determinism detection 
toolchain (*NDDetector*) used in RQ2. 

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

*Note: There were 58 issues of Doop (as of the time this research was conducted) that are hosted on [BitBucket](https://bitbucket.org/yanniss/doop-deprecated/issues), as stated at the beginning of Section III of our paper. These issues are not included in `raw_data.zip` as BitBucket requires administrative access to the repository to export the issues.*

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

The `code` directory includes two sub-directories, `Git_Extractor` and `NDDetector`.

The scripts under `Git_Extractor` folder are used in RQ1 to extract the issues and commits from each tool's GitHub repository.  
The source code under `NDDetector` folder is the non-determinism detection toolchain (*NDDetector*) used in RQ2.

*NDDetector* is a flexible tool that can be used to detect non-deterministic behaviors in configurable static analysis on a variety of benchmarks. 
*NDDetector* can be extended to use alternative analyses, but currently, it can run call graph analyses using WALA, SOOT, DOOP, OPAL, TAJS, PyCG, and Code2Flow, 
taint analysis on Android applications using FlowDroid, AmanDroid, and DroidSafe, as well as vulnerability detection on C programs using Infer.

### Requirements

- Hardware: This artifact requires Linux or macOS systems with Intel processors to conduct the experiments.
- Software:
  - A Python executable of version 3.10.x, including the venv and development packages (`python3.XX-dev` and `python3.XX-venv` on Ubuntu). 
Note that if you installed via `brew` or the Windows installer, your Python should already have these.
  - A C and C++ compiler, e.g., `gcc` and `g++`.
  - GNU `Make`

For example, setting up these dependencies on Ubuntu 22.04 looks like:

```commandline
sudo apt install python3.10 python3.10-dev python3.10-venv g++ gcc make cmake
```
In addition, you must have a working Docker installation (https://docs.docker.com/get-docker/).

### Instructions

#### RQ1: Extract Issues and Commits

To extract the issues and commits from each tool's GitHub repository that are used in RQ1, follow the below steps:

Navigate to the `code/Git_Extractor` folder:

`cd code/Git_Extractor`

Then install the Python dependencies, run: 

`python -m pip install -r requirements.txt`

#### RQ2: Detect Nondeterminisms

To set up the nondeterminism detection framework, we recommend creating a virtual environment. 

To do so, navigate to the `code/NDDetector` folder:

`cd code/NDDetector`

Then, run: 

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

The description for the arguments/options of the `dispatcher` are as follows:

```
options:
  -h, --help            Show this help message and exit.
  -t, --tools           Static analysis tools to run. Options:
                        {flowdroid,amandroid,droidsafe,soot,wala,doop,opal,code2flow,pycg,tajs,wala-js,infer} 
  -b, --benchmarks      Benchmark programs to run, incompatible tool and benchmark pairs will be skipped. Options:
                        {icse25-ezbench,droidbench,fossdroid-all-apks,icse25-ezcats,cats-microbenchmark,dacapo-2006,pycg-micro,pycg-macro,sunspider_test,jquery,
                         itc-benchmarks,openssl,toybox,sqlite} 
  --tasks               Currently a useless option as all tools only support one task. However, this is meant to provide support for tools
                        that might allow multiple tasks. Options:
                        {cg,taint,violation}
  --no-cache, -n        Build images without cache.
  --jobs JOBS, -j JOBS  Number of jobs to spawn in each container.
  --iterations ITERATIONS, -i ITERATIONS
                        Number of iterations to run.
  --timeout TIMEOUT     The timeout to pass to the static analysis tool in minutes.
  --verbose, -v         Level of verbosity (more v's gives more output)
  --results RESULTS     Location to write results.
  --nondex              Run java tools with NonDex.
```


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

***For artifact reviewers:*** 
We provide smaller experiments to verify the functionality of the artifact in the `Basic Usage Example` section, as replicating the major paper results is expected to take thousands of hours of machine time.

### Basic Usage Example

We suggest artifact reviewers use FlowDroid or SOOT, as these tools are relatively faster and more likely to exhibit nondeterministic behaviors compare to other tools, which tend to be slower to build, require significant system memory, or are challenging for capturing nondeterminism.

We have provided small versions of the Droidbench and CATS Microbenchmark under the names `icse25-ezbench` and 
`icse25-ezcats`, respectively. These benchmarks each contain one program that exhibited nondeterministic behaviors:

- `icse25-ezbench` contains *JavaThread2.apk*.
- `icse25-ezcats` contains *TC1.jar*.

#### Detecting Nondeterminism Using Strategy I

First, ensure that you are in the `code/NDDetector` directory.

Then, to run FlowDroid on `icse25-ezbench` using Strategy I (as discussed in Section IV.A.d in our paper), run the following command:

```commandline
# Expected running time is around 10-15 minutes.
dispatcher -t flowdroid -b icse25-ezbench --tasks taint -i 5 
```

To run SOOT on `icse25-ezcats` using Strategy I, run the following command:

```commandline
# Expected running time is around 10-20 minutes.
dispatcher -t soot -b icse25-ezcats --tasks cg -i 5
```
where `-i 5` can be configured to the number of iterations you wish to run. This will create a `results` folder. Details on how to read the contents of this folder are below.

#### How to Read Output

By default, the output will be stored in a *results* folder, but the location of the results can be controlled with the `--results-location` option.

We explain the structure of the results through the FlowDroid example above, where we run FlowDroid on the `icse25-ezbench` benchmark.

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
|- non_determinism
|  |- flowdroid
|  |  |- icse25-ezbench
|  |  |  |- 7b5480bdb06b2ff39ebfb2bcedd2f657_JavaThread2.apk.raw
|  |  |  |  |- run-0
|  |  |  |  |- run-1
|  |  |  |  |- ...
```

The results of each iteration are stored in their respective folders. For each configuration-program pair, three files are generated, each with a different extension: `.raw`, `.raw.log`, and `.raw.time`. These files correspond to the results produced by the tool, which will be processed by the *ToolReader* implementation, the log for each experiment, and the execution time for each experiment, respectively.

Configurations in the results are represented as hash values. You can see what configuration a hash value represents by looking in the configuration folder. In this example, configuration 1e9c00f5704518e138859b037784c841 corresponds to the configuration `--aplength 10 --cgalgo RTA --nothischainreduction --dataflowsolver CONTEXTFLOWSENSITIVE --aliasflowins --singlejoinpointabstraction --staticmode CONTEXTFLOWSENSITIVE --nostatic --codeelimination PROPAGATECONSTS --implicit ALL --callbackanalyzer FAST --maxcallbackspercomponent 1 --maxcallbacksdepth 1 --enablereflection --pathalgo CONTEXTSENSITIVE --taintwrapper NONE`

The results of non-determinism detection can be found in the `non_determinism` folder *(if any nondeterminism is detected)*. 

This folder maintains all non-deterministic results across 5 iterations, each batch of results is stored under a folder named as `configration-hash_apk-name.apk.raw`.

***Note: Nondeterminisms may not be reproduced without running the software multiple times. And the detected nondeterminisms may vary across experiments for the same tool-benchmark pair.***

In our example, one detected non-determinism is on `JavaThread2.apk` under configuration  `7b5480bdb06b2ff39ebfb2bcedd2f657`.

#### Detecting Nondeterminism Using Strategy II

To get the addtional nondeterminism using Strategy II (as discussed in Section IV.A.d in our paper), run FlowDroid on `icse25-ezbench` with NonDex enabled: 

```commandline
# Expected running time is around 10-15 minutes.
dispatcher -t flowdroid -b icse25-ezbench --tasks taint -i 5 --results ./results_nondex --nondex
```
To run SOOT on `icse25-ezcats` with NonDex enabled:

```commandline
# Expected running time is around 60-90 minutes.
dispatcher -t soot -b icse25-ezcats --tasks cg -i 5 --results ./results_nondex --nondex
```
This will create a `results_nondex` folder which contains the new experiment results. 

***Note: The results in the `results_nondex/non_determinism` folder are not yet the final additional nondeterminism detected by Strategy II, as discussed in Section IV.A.d of our paper.***

To get the final addtional nondeterminism using Strategy II, navigate to the `scripts/analysis` directory:

`cd scripts/analysis`

The script `detector_strategy_2.py` is used to detect additional nondeterminisms from the new results (as discussed at the end of Section IV.A.d in our paper).

Run the following commands to detect the additional nondeterminisms for FlowDroid and SOOT:

```
python detector_strategy_2.py --origin ../../results --nondex ../../results_nondex flowdroid icse25-ezbench taint 5
python detector_strategy_2.py --origin ../../results --nondex ../../results_nondex soot icse25-ezcats cg 5
```

These commands output the detected additional nondeterminisms (using Strategy II) to the `results_II/non_determinism` folder within the `code/NDDetector` directory *(if any additional nondeterminism is detected)*.

#### Post-processing Results

In the `scripts/analysis` directory, the script `post_process.py` aggregates the detected nondeterminism results for each specified tool-benchmark pair for both strategies.

Run the following commands to generate aggregated results for all nondeterminisms detected above:

```
# if any nondeterminism is detected by running FlowDroid on icse25-ezbench using Strategy I
python post_process.py --path ../../results/non_determinism flowdroid icse25-ezbench

# if any additional nondeterminism is detected by running FlowDroid on icse25-ezbench using Strategy II
python post_process.py --path ../../results_II/non_determinism flowdroid icse25-ezbench --nondex

# if any nondeterminism is detected by running SOOT on icse25-ezcats using Strategy I
python post_process.py --path ../../results/non_determinism soot icse25-ezcats

# if any additional nondeterminism is detected by running SOOT on icse25-ezcats using Strategy II
python post_process.py --path ../../results_II/non_determinism soot icse25-ezcats --nondex
```
Each command generates a CSV file named `<tool>_<benchmark>.csv` or `<tool>_<benchmark>_nondex.csv` in the `postprocess` folder within the `code/NDDetector` directory (*if the provided nondeterminism folder exists*). It calculates the percentage of consistent results and the number of distinct results.

### Replicating Major Paper Results

Replicating the major results from the paper is expected to require thousands of hours of machine time and significant system memory. Please ensure that sufficient computing resources are available before running these commands. For reference, the experiments in our paper were conducted on two servers:  

- *Server 1*: 384GB of RAM, 2 Intel Xeon Gold 5218 16-core CPUs @ 2.30GHz.  
- *Server 2*: 144GB of RAM, 2 Intel Xeon Silver 4116 12-core CPUs @ 2.10GHz.  

*Note that as of this writing, PyCG experiments cannot be replicated due to errors encountered when running PyCG on the Ubuntu system. 
We haven't been able able to fix it because PyCG has been archived and is no longer maintained by its development team.*

The following 24 commands will run experiments for all tool/benchmark combinations using Strategy I, excluding PyCG. Alternatively, you can execute the shell script `run_all_s1.sh`. 

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

The next 8 commands will run experiments for all compatible analysis tool/benchmark combinations with NonDex enabled. This includes running Soot, FlowDroid, Amandroid, and TAJS on their respective benchmarks. Alternatively, you can execute the shell script `run_all_s2.sh`.

```commandline
dispatcher -t flowdroid -b droidbench --task taint -j 10 -i 5 --timeout 5 --results ./results_nondex --nondex
dispatcher -t flowdroid -b fossdroid-all-apks --task taint -j 10 -i 5 --timeout 60 --results ./results_nondex --nondex

dispatcher -t amandroid -b droidbench --task taint -j 10 -i 5 --timeout 5 --results ./results_nondex --nondex
dispatcher -t amandroid -b fossdroid-all-apks --task taint -j 10 -i 5 --timeout 60 --results ./results_nondex --nondex

dispatcher -t soot -b cats-microbenchmark --task cg -j 10 -i 5 --timeout 15 --results ./results_nondex --nondex
dispatcher -t soot -b dacapo-2006 --task cg -j 10 -i 5 --timeout 120 --results ./results_nondex --nondex

dispatcher -t tajs -b sunspider_test --task cg -j 10 -i 10 --timeout 5 --results ./results_nondex --nondex
dispatcher -t tajs -b jquery --task cg -j 10 -i 10 --timeout 120 --results ./results_nondex --nondex
```
Then, navigate to the `scripts/analysis` directory.

Run the following command to detect additional nondeterminisms using Strategy II:

```
python detector_strategy_2.py --origin <path-to-strategy-I-results-folder> --nondex <path-to-nondex-results-folder> <tool> <benchmark> <task> <iteration>
```
This command outputs the detected additional nondeterminisms to the `results_II/non_determinism` folder within the `code/NDDetector` directory.

We run this script for all compatible analysis tool/benchmark combinations for Strategy II. This includes running Soot, FlowDroid, Amandroid, and TAJS on their respective benchmarks.

The results from all the above steps correspond to those presented in Tables V and VI.

Next, run the following commands to aggregate Strategy I and II results for each specified tool-benchmark pair, respectively:

```
# Aggregate Strategy I results.
python post_process.py --path <path-to-strategy-I-non_determinism-folder> <tool> <benchmark>

# Aggregate Strategy II results.
python post_process.py --path <path-to-strategy-II-non_determinism-folder> <tool> <benchmark> --nondex
```

Each command generates a CSV file in the `postprocess` folder within the `code/NDDetector` directory, aggregating all results for the specified tool-benchmark pair. It also calculates the percentage of consistent results and the number of distinct results.

We run this command for every tool-benchmark pair for Strategy I and II, if its respective nondeterminism folder exists. These results are then consolidated into a single file: `ICSE2025_AGGREGATE_DATA.csv`.

Additionally, we provide a Jupyter notebook, `scripts/notebooks/graphs.ipynb`, to generate figures 3 and 4 for `RQ2.2`. This notebook requires `ICSE2025_AGGREGATE_DATA.csv` as input, containing all results from the CSVs generated by the `post_process.py` script. It is designed to work with the complete dataset, including non-determinism data from all eight tools discussed in the paper.

### Troubleshooting

If you encounter errors regarding `docker login: denied: requested access to the resource is denied` while using this project, refer to the common troubleshooting steps below:

1. Check if the current user is in the `docker` group:

```sh
groups $(whoami)
```

2. If the current user is not in the docker group, add them:

```sh
sudo usermod -aG docker $USER
```

If the above step does not resolve this issue, you can run docker in rootless mode and then run the experiment using the following steps:

1. Install dependency uidmap, which handles the user namespace mapping for the system:

```sh
sudo apt-get install uidmap -y
```

2. Install rootless docker:

```sh
curl -fsSL https://get.docker.com/rootless | sh
```

3. Add the following environment variables to `~/.bashrc`:

```sh
export PATH=/home/$USER/bin:$PATH
export DOCKER_HOST=unix:///run/user/$ID/docker.sock
```
   The `$ID` is the current user ID which can be obtained by running `id`.

4. Close `~/.bashrc` and run `source ~/.bashrc` for the changes to take effect.

5. Use `systemctl --user status docker` to check if rootless docker is running successfully.

6. Re-run experiments under rootless docker mode.




