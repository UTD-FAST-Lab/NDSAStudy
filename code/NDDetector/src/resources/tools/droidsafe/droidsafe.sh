#!/bin/bash

# Parameter:
# 1: .apk file
# 2: App name without .apk
# 3: Arguments to pass to DroidSafe

# The following environmental variables must be set.
# DROIDSAFE_SRC_HOME, which must point to the droidsafe-src directory.
# ANDROID_SDK_HOME, which must point to the platforms directory.

# Create folder structure
mkdir $DROIDSAFE_SRC_HOME/runs/${2} -p
cd $DROIDSAFE_SRC_HOME/runs/${2}
cp ${1} .

# Create AndroidManifest.xml
f="$(basename -- ${1})"
apktool d ./${f}
filename="${f%.*}"
cp ./${f} ./${filename}
cd $DROIDSAFE_SRC_HOME/bin

# Run droidsafe 
python droidsafe ${3} -noarrayindex -nojsa -noscalaropts -approot $DROIDSAFE_SRC_HOME/runs/${2}/${filename} -apk
