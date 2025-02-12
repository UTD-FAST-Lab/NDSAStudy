#!/bin/bash

LIST=(
    "Soot"
    "Wala" 
    "Doop"
    "opal"
    "FlowDroid" 
    "DroidSafe" 
    "AmanDroid" 
    "TAJS" 
    "PyCG" 
    "Code2flow"
    "infer"
    )

for VALUE in "${LIST[@]}"
do 
    echo "Exporting ${VALUE}_issues ..."
    mongoexport --collection ${VALUE}_issues --pretty --out ./${VALUE}_issues.json --uri ${DB_CONNECTION_STRING_EXPORT}/NdGit
done

