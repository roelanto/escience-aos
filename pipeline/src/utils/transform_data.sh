#!/usr/bin/env bash

# This script creates a total of 10 files for each folder
# in the source folder from data/train/raw or data/test/raw
# and writes these to the destination folder
# data/train/final or data/test/processed.
# Of the 10 files, 4 will be common files for each of the subfolders
# in the destination folder. The other 4 3-digit sequencies will 
# be randomly chosen

if [ $# != 2 ]; then
    echo "Use like this:"
    echo "transform_data.sh <src_dir> <dst_dir>"
    echo "e.g.: transform_data.sh train/raw train/final"
    exit 1
fi

cd data/$1

# 1. Create function to update 3 global random numbers
gen_3_rand_num(){
    n1=$((0 + $RANDOM % 10))
    n2=$((0 + $RANDOM % 10))
    n3=$((0 + $RANDOM % 10))
}

# 2. For each speaker
for speaker in */; do 
    cd $speaker
    # 3. Create the common files
    sox "0.wav" "1.wav" "2.wav" "../../../$2/$speaker/0_1_2.wav"
    sox "3.wav" "4.wav" "5.wav" "../../../$2/$speaker/3_4_5.wav"
    sox "6.wav" "7.wav" "8.wav" "../../../$2/$speaker/6_7_8.wav"
    sox "9.wav" "0.wav" "1.wav" "../../../$2/$speaker/9_0_1.wav"
    # 4. Create 6 files with random sequences
    for i in {0..5}; do 
        gen_3_rand_num # 5. Generate random sequence of 3 numbers
        while [ -f "../../../$2/$speaker/"$n1"_"$n2"_"$n3".wav" ]
        do
            gen_3_rand_num
        done # 6. Concatenate random sequence of 3 numbers
        sox $n1".wav" $n2".wav" $n3".wav" "../../../$2/$speaker/"$n1"_"$n2"_"$n3".wav"
    done
    cd ..
done