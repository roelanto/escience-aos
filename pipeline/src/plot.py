"""
    Functions regarding any kind of plotting, will
    be stored here.
"""

import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import numpy as np
import pandas as pd
from src.file_frame import get_samples, get_time_samples
from src.sample import get_formants, get_hpf_hamm_win_samples
import librosa
import os
from typing import Tuple
from dotenv import load_dotenv
load_dotenv()

digits_path = os.getenv("DIGITSPATH")

def plot_raw_wave(**kwargs) -> None:
    """
    This function plots the raw wave of an audio file

    Parameters
    ----------
        df: pd.DataFrame
            dataframe with the audio files, speakers and samples
        speaker: str
            speaker for which an audio file must be plotted
        audio_file: str
            audio file that must be plotted
        model: str
            asr model (mono/tri1)
        ax: plt.Axes
            ax on which the plot must be set
        with_phones: bool
            plot the time aligned phone transcription
        with_words: bool
            plot the time aligned word transcription
    
    Example
    -------
    >>> plot_raw_wave_temp(df=df_files, speaker="jackson", audio_file="0_1_2.wav", 
    model="mono", ax=ax, with_phones=True, with_words=True)

    Plots the raw wave of audio file, for speaker on ax with phone and word aligned transcriptions
    """
    try:
        df              = kwargs["df"]
        speaker         = kwargs["speaker"]
        audio_file      = kwargs["audio_file"]
        model           = kwargs["model"]
        ax              = kwargs["ax"]
        with_phones     = kwargs["with_phones"]
        with_words      = kwargs["with_words"]
        samples         = get_samples(df, speaker, audio_file)
        time            = get_time_samples(samples)
        t_path               = None
        plot_raw_wave.factor = 2

        librosa.display.waveshow(y=samples, sr=8000, ax=ax, color='C1', x_axis='time')
        ax.set_title('Raw wave form')
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Amplitude')
        ax.set_xlim([time[0], time[-1]])

        def plot_time_aligned_transcription(
            speaker: str, audio_file: str, time: np.array, ax: plt.Axes) -> None:
            """Plots the transcription along the time"""
            with open(t_path, "r") as f:
                transcript = [line for line in f.readlines() if f"{speaker}_{audio_file[:-4]}" in line]
                transcript = [ # (t0, tend, <transcribed phone/word>)
                    (float(line.split(" ")[2]), float(line.split(" ")[2])+float(line.split(" ")[3]), line.split(" ")[4])
                    for line in transcript
                ]
                for t in transcript:
                    ax.axhline(y=ax.get_ylim()[1]/plot_raw_wave.factor, xmin=t[0]/time[-1], xmax=t[1]/time[-1], color="purple")
                    ax.text(x=(t[0]+t[1])/2, y=ax.get_ylim()[1]/(plot_raw_wave.factor*0.85), s=t[2], fontsize=12)
                    ax.scatter(t[:2], [ax.get_ylim()[1]/plot_raw_wave.factor, ax.get_ylim()[1]/plot_raw_wave.factor], marker="o", c="purple")
                plot_raw_wave.factor*=2
                f.close()

        if with_phones: 
            t_path=digits_path + f"/time_marked_transcript_{model}_phones.ctm" 
            plot_time_aligned_transcription(speaker=speaker, audio_file=audio_file, 
                                            time=time, ax=ax)
        if with_words: 
            t_path=digits_path + f"/time_marked_transcript_{model}_words.ctm" 
            plot_time_aligned_transcription(speaker=speaker, audio_file=audio_file,
                                            time=time, ax=ax)
    except KeyError:
        raise KeyError(help(plot_raw_wave))

def plot_fig(figsize: Tuple[int, int], f, *args) -> None:
    """
    Plot one or multiple plots in one figure

    Parameters
    ----------
        figsize: Tuple[int, int]
            size of the eventual figure
        f: List[Callable[[Any], None]]
            list of plot functions that need to be used
        args: List[Dict[str, Any]]
    
    Example
    -------
    >>> plot_fig([plot_raw_wave_temp, plot_raw_wave_temp], 
    [{"df":df_files, "speaker":"jackson", "audio_file":"0_1_2.wav", 
    "model":"mono", "with_phones":True, "with_words":True}, 
    {"df":df_files, "speaker":"jackson", "audio_file":"0_1_2.wav", 
    "model":"mono", "with_phones":True, "with_words":True}])

    Plots two identical raw waves underneath eachother
    """
    rows = len(f)
    fig, ax = plt.subplots(ncols=1, nrows=rows, figsize=figsize)
    for i, (func, arg) in enumerate(zip(f, *args)):
        arg["ax"] = ax[i]
        func(**arg)
    plt.show()

def plot_spectrogram(**kwargs) -> None:
    """
    Plots the spectrogram of a partitian of an audio file with the formants
    
    Parameters
    ----------
        samples: np.array
            sampled audio data
        ax: plt.Axes
            ax on which plot must be plotted
        dt_0: float
            start of the range for which the spectrogram must be plotted
        dt_end: float
            end of the range for which the spectrogram must be plotted
        formants: bool
            show formants
    
    Example
    -------
    >>> plot_spectrogram(samples=[.0,...,0.1], ax=ax, dt_0=.0, dt_end=1.2, formants=True)

    Plots the spectrogram of the audio samples on ax with the found formants
    """
    try:
        samples             = kwargs["samples"]
        ax                  = kwargs["ax"]
        dt_0                = kwargs["dt_0"]
        dt_end              = kwargs["dt_end"]
        formants            = kwargs["formants"]
        time                = get_time_samples(samples)
        sr                  = 8000
        pxx, freq, t, cax   = ax.specgram(x=samples, Fs=sr, cmap='plasma')
        intensity_bar       = plt.colorbar(cax, ax=ax)
        ax.set_title('Mel Spectrogram')
        ax.set_ylabel('Frequency [Hz]')
        ax.set_xlabel('Time [s]')
        intensity_bar.set_label("Intensity [dB]")
        if formants:
            for min in np.arange(dt_0, dt_end, (dt_end - dt_0)/40):
                _, p = get_formants(samples, min, min+((dt_end - dt_0)/40))
                ax.scatter([min+(((dt_end - dt_0)/40)/2) for _ in p], p, marker=">", c='black')
        ax.set_xlim([time[round(dt_0/(1/sr)) if dt_0 > 0 else 0], time[round(dt_end/(1/sr))]])
    except KeyError:
        raise KeyError(help(plot_spectrogram))

def plot_windowed_samples(**kwargs) -> None:
    """
    Plots the Hamming windowed samples of a time range

    Parameters
    ----------
        samples: np.array
            sampled audio data
        ax: plt.Axes
            ax on which plot must be plotted
        dt_0: float
            start of the range for which the spectrogram must be plotted
        dt_end: float
            end of the range for which the spectrogram must be plotted

    Example
    -------
    >>> plot_windowed_samples(samples=[.0,...,0.1], ax=ax, dt_0=.0, dt_end=1.2)

    Plots the Hamming windowed samples
    """
    samples     = kwargs["samples"]
    ax          = kwargs["ax"]
    dt_0        = kwargs["dt_0"]
    dt_end      = kwargs["dt_end"]
    ax.plot(get_hpf_hamm_win_samples(samples, dt_0, dt_end), color='C1')
    ax.set_title(f"Hamming Windowed samples of [{round(dt_0, 3)},{round(dt_end, 3)}]")
    ax.set_ylabel('Amplitude')
    ax.set_xlabel('Time [samples]')

def plot_magnitude_spectrum(**kwargs) -> None:
    """
    Plots the magnitude spectrum of an audio signal with the formants

    Parameters
    ----------
        samples: np.array
            sampled audio data
        fig: plt.Figure
            figure in which the formants must be plotted
        ax: plt.Axes
            ax on which plot must be plotted
        dt_0: float
            start of the range for which the spectrogram must be plotted
        dt_end: float
            end of the range for which the spectrogram must be plotted
        eps: float
            multiplying factor for approaching the formants
    
    Example
    -------
    >>> plot_magnitude_spectrum(samples=[.0,...,0.1], fig=fig, ax=ax, dt_0=.0, dt_end=1.2, eps=0.1)

    Plots the magnitude spectrum of the sampled audio data along with the formants found in the spectrum
    """
    samples         = kwargs["samples"]
    fig             = kwargs["fig"]
    ax              = kwargs["ax"]
    dt_0            = kwargs["dt_0"]
    dt_end          = kwargs["dt_end"]
    eps             = kwargs["eps"]
    win_hpf         = get_hpf_hamm_win_samples(samples, dt_0, dt_end)
    envelope, peaks = get_formants(samples, dt_0, dt_end, eps)
    formant_labels  = ['F1', 'F2', 'F3']
    ax.magnitude_spectrum(win_hpf, Fs=8000, scale='dB', color='C1')
    ax.set_title('Log Magnitude Spectrum of windowed samples')
    ax.set_ylabel('Magnitude [dB]')
    ax.set_xlabel('Frequency [Hz]')
    ax.plot(envelope, color='C2')
    ax.scatter(peaks, envelope[peaks], marker='o', c='black', s=50)
    for i, (xi, yi) in enumerate(zip(peaks, envelope[peaks])):
        plt.text(xi, yi, f'↙ {formant_labels[i]}', 
        transform=mtransforms.offset_copy(ax.transData, fig=fig, x=0.3, y=0.1), 
        va='center', ha='center', fontsize=14)