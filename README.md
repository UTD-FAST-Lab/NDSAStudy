# ICSE2025
Artifact for An Extensive Empirical Study of Nondeterministic Behavior in Static Analysis Tools.

This repository contains the code and data for the paper titled 'An Extensive Empirical Study of Nondeterministic Behavior in Static Analysis Tools,'. 

The code directory contains the zipped source code of the nondeterminism detection framework (NDDetector) used in RQ2. To maintain anonymity, we have anonymized links in the source code used to access external tools and benchmarks, so the full experiments are not functional in this version of the artifact. We plan to make a submission to the artifact evaluation track upon acceptance of our paper with all the experiments working.

The data directory contains files that support the conclusions made in the two research questions (RQ1 and RQ2). Inside the data directory, there are two sub-directories (rq1 and rq2):

In rq1/ there are:

RQ1_FINAL_RESULTS.csv - Contains 85 distinct results from 7 repositories (SOOT, WALA, DOOP, OPAL, FlowDroid, DroidSafe, Infer) that fix or report nondeterminism, each result is an issue with ID, tool name, linked issues/commits, root cause category, and pattern.

RQ1_ND_PATTERN_LIST.pdf - Contains 9 distinct common patterns of nondeterminism, each pattern is described with a pattern ID, description, solution, occurrence in each tool, related results, and a code example.

raw_data.zip - Contains the raw commits and issues extracted from 11 repositories (SOOT, DOOP, WALA, OPAL, FlowDroid, DroidSafe, AmanDroid, TAJS, Code2Flow, PyCG, Infer).

key_words_results.zip - Contains the results extracted by each keyword (concurrency, concurrent, determinism, deterministic, flakiness, flaky) from the raw data.

In rq2/ there are two sub-directories (rq2.1 and rq2.3):

In rq2.1/ there are:

RQ2_AGGREGATE_DATA.csv - Contains the result distributions of each combination of target program, configuration hash, and tool as well as the calculated consistency score.

In rq2.3/ there are:

12 PDF files of each reported issues discussed in RQ2.3, including 3 FLowDorid issues, 2 SOOT issues, 1 issue for DOOP, OPAL, Infer, Amandroid, PyCG and Code2Flow each. Additionally, there is an email from a FlowDroid developer, serving as a response to the FlowDroid-reported-issue-3. We have tried to anonymize all identifiable information such as IDs, names, or links to maintain confidentiality.

