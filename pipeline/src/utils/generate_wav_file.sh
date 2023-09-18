#!/usr/bin/env bash

. ./path.sh || exit 1

# This script goes through every utterance made 
# and creates a file named wav.scp with a mapping
# between each speaker with their utterance followed
# by the full path to the corresponding audio file

cd ../$DIGITS_ROOT/data/train

# 1. Only execute if wav.scp doesn't exist yet
if [ ! -f "wav.scp" ]; then
    touch wav.scp # 2. Create file
    cd ../../digits_audio
    for subd in */ ; do # 3. For the train and test folder
        cd $subd
        for speaker in */ ; do # 4. For each speaker
            cd $speaker
            for audio in * ; do # 5. For each audio made by speaker
                #                    Save their utterance ID with the full path
                #                    to the audio file.
                filename=$(basename $audio .wav)
                s=$(basename $speaker /)
                path=$(pwd)
                echo $s"_"$filename $path"/"$filename".wav" >> ../../../data/train/wav.scp
            done
            cd ..
        done
        cd ..
    done
    cd ../data/train
fi