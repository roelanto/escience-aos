"""
    Functions regarding using the audio samples,
    are defined here.
"""

import numpy as np
import librosa
from scipy import signal
from typing import Tuple

def get_time_samples(samples: np.array) -> np.ndarray:
    """Returns an array with for each sample the corresponding time stamp"""
    length = samples.shape[0] / 8000
    return np.linspace(0., length, samples.shape[0])

def get_formants(samples: np.array, dt_0: float, dt_end: float, eps=1e1) -> Tuple[np.ndarray, list]:
    """
        Computes the vowel formants using the LPC Auto Regressive model.

        Parameters
        ----------
            samples: np.array
                Used to retrieve the envelope of the spectrum
            dt_0 : float
                Forms with dt_end the time range of the file for which formants must be computed
            dt_end : float
                Forms with dt_0 the time range of the file for which formants must be computed
        
        Returns
        -------
            Envelope of the spectrum of the audio file with the formants

    """
    sr           = 8000 # Sample rate
    y            = samples
    order        = 10 # Determines the accuracy of the formants. Values 10 & 12 are most accurate
    dt           = 1/sr 
    I0           = round(dt_0/dt)
    Iend         = round(dt_end/dt)
    worN         = sr//2 # Computes at this number of frequencies

    a = librosa.lpc(y[I0:Iend], order)
    freqs, h = signal.freqz(1.0, a, worN)
    envelope = 20*np.log10((np.abs(h)/np.max(np.abs(h)))*eps)
    envelope[envelope<-120] = -120

    peaks, _ = signal.find_peaks(envelope)
    peaks = peaks[peaks > 90]
    peaks = [np.where(envelope == p)[0][0] for p in sorted(envelope[peaks], reverse=True)[:3]]
    return envelope, peaks

def get_hpf_hamm_win_samples(samples: np.array, dt_0: float, dt_end: float) -> np.array:
    """Windows audio signal after applying high pass filter"""
    dt      = 1/8000
    F0      = round(dt_0/dt)
    Fend    = round(dt_end/dt)
    time    = get_time_samples(samples)
    N       = len(time[F0:Fend])
    win     = np.hamming(N)
    win_hpf = samples[F0:Fend] * win
    win_hpf = signal.lfilter([1], [1., 0.63], win_hpf)
    return win_hpf