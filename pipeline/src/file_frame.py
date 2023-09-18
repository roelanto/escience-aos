"""
    Functions regarding building, updating and retrieving
    from the dataframe `df_files` are stored here.
"""

import os
import librosa
import numpy as np
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

digits_path = os.getenv("DIGITSPATH")


def update_file_frame(df: pd.DataFrame) -> None:
    """
    Updates the dataframe of files by 
    overwriting existing files or adding 
    new audio files for each speaker found in
    the test and train set.
    """
    for dataset in os.listdir(digits_path + "/digits_audio"):
        for speaker in os.listdir(digits_path + "/digits_audio/" + dataset):
            for file in os.listdir(digits_path + "/digits_audio/" + dataset + "/" + speaker):
                samples, _ = librosa.load(digits_path + "/digits_audio/" + dataset + "/" + speaker + "/" + file, sr=8000, mono=True)
                samples = np.array(samples, dtype=object)
                df.at[(speaker, dataset, file), ('samples', 'duration')] = [samples, samples.shape[0]/8000]

def get_set_speaker(df: pd.DataFrame, speaker: str) -> str:
    """Returns the set of a speaker from dataframe"""
    return df.xs(speaker, level=0, axis=0).index.unique(level=0)[0]

def get_samples(df: pd.DataFrame, speaker: str, audio_file: str) -> np.array:
    """Returns the samples of audio_files of speaker from dataframe"""
    return np.array(df.loc[(speaker, get_set_speaker(df, speaker), audio_file),
    ('samples')], dtype=np.float32)

def get_time_samples(samples: np.array) -> np.ndarray:
    """Returns an array with for each sample the corresponding time stamp"""
    length = samples.shape[0] / 8000
    return np.linspace(0., length, samples.shape[0])