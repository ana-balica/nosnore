#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SAMPLES_PATH="/../samples/ucddb/"
CURRPATH=$DIR$SAMPLES_PATH
cd $CURRPATH

TRAIL="_recm.info"

for f in `ls *.rec`
do
    IFS='.' read -a base_name <<< "${f}"
    wfdb2mat -r $f -f 0 -s Sound > ${base_name[0]}$TRAIL
done
