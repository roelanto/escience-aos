#!/usr/bin/env bash

# This script retrieves the training data from the FSDD repository
# and stores it in the directory: data/train/raw

cd data/train/raw

LINK="https://github.com/Jakobovski/free-spoken-digit-dataset/raw/master/recordings/"

for speaker in */; do
    cd "$(basename $speaker)"
    for digit in {0..9}; do
        [ ! -f "$digit.wav" ] && wget -O "$digit.wav" $LINK$digit"_$(basename $speaker)_0.wav"
    done
    cd ..
done