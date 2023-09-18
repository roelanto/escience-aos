#!/usr/bin/env bash

. ./path.sh || exit 1

# This script creates the time aligned transcription with 
# confidence scores on phone level
# for an ASR model

if [ $# != 1 ]; then
    echo "Use like this:"
    echo "generate_phone_ctm_conf.sh <mono/tri1>"
    exit 1
fi

cd ../$DIGITS_ROOT

../../src/latbin/lattice-align-phones --replace-output-symbols=true \
exp/$1/final.mdl "ark:zcat exp/$1/decode/lat.1.gz|" ark:- | \
../../src/latbin/lattice-to-nbest ark:- ark:- | \
../../src/latbin/lattice-to-ctm-conf --acoustic-scale=0.8 ark:- - | \
utils/int2sym.pl -f 5 data/lang/phones.txt > tmt_conf_$1_phones.ctm