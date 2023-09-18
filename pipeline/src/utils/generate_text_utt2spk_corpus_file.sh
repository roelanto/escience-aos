#!/usr/bin/env bash

. ./path.sh || exit 1

# This script creates the text, utt2spk and corpus file
# for the audio data

cd ../$DIGITS_ROOT/data/train

declare -A vocab
vocab[0]="zero"
vocab[1]="one"
vocab[2]="two"
vocab[3]="three"
vocab[4]="four"
vocab[5]="five"
vocab[6]="six"
vocab[7]="seven"
vocab[8]="eight"
vocab[9]="nine"

filename="wav.scp"
lines=$(cat $filename)

# 1. If the text file doesn't exist yet
if [ ! -f text ]; then 
    touch text
    counter=0
    for line in $lines; do # 2. Retrieve the speaker and spoken number from wav.scp
        if ((counter%2 == 0)); then 
            nums="${line//[^0-9.]/}"
            if [ ${#nums} == 4 ]; then # Don't use the numbers 1 and 2 of the speakers
                nums=${nums:1:3}       # in the test set
            fi
            n1=${nums:0:1}
            n2=${nums:1:1}
            n3=${nums:2:1}
            # 3. Concatenate each of the speakers and their utterances to 
            #    the text file and all transciptions to corpus.txt 
            #    (this means that repeated utterances can appear more than once in the corpus file)
            echo $line ${vocab[$n1]} ${vocab[$n2]} ${vocab[$n3]} >> text
            cd ../local;[ ! -f corpus.txt ] || touch corpus.txt;echo ${vocab[$n1]} ${vocab[$n2]} ${vocab[$n3]} >> corpus.txt
            cd ../train
            speaker=$(cut -d _ -f 1 <<< $line)
            [ ! -f utt2spk ] || touch utt2spk;echo $line $speaker >> utt2spk
        fi
        ((counter=counter+1))
    done
fi