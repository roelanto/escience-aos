#!/usr/bin/env bash

. ./path.sh || exit 1

# This script creates the time aligned transcription on word level
# for an ASR model

if [ $# != 1 ]; then
    echo "Use like this:"
    echo "generate_word_ctm.sh <mono/tri1>"
    exit 1
fi

cd ../$DIGITS_ROOT

../../src/latbin/lattice-1best --lm-scale=0.1 \
              "ark:zcat exp/$1/decode/lat.1.gz|" ark:- | \
../../src/latbin/lattice-align-words data/lang/phones/word_boundary.int \
                    exp/$1/final.mdl \
                    ark:- ark:- | \
../../src/latbin/nbest-to-ctm ark:- - | \
utils/int2sym.pl -f 5 data/lang/words.txt > time_marked_transcript_$1_words.ctm