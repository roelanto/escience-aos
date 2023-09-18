#!/usr/bin/env bash

. ./path.sh || exit 1

# This script creates the time aligned transcription on phone level
# for an ASR model

if [ $# != 1 ]; then
    echo "Use like this:"
    echo "generate_phone_ctm.sh <mono/tri1>"
    exit 1
fi

cd ../$DIGITS_ROOT

../../src/latbin/lattice-align-phones --replace-output-symbols=true \
exp/$1/final.mdl "ark:zcat exp/$1/decode/lat.1.gz|" ark:- | \
../../src/latbin/lattice-1best ark:- ark:-| \
../../src/latbin/nbest-to-ctm ark:- - | \
utils/int2sym.pl -f 5 data/lang/phones.txt > \
time_marked_transcript_$1_phones.ctm