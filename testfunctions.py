""" Functions I could need in the main code
"""
from brian2 import *
from parameters import *
import numpy as np
from scipy.signal import welch, filtfilt, butter

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def firingrate(spikemonitor, sim_time):
    """ Calculte the firing rate over the
        entire simulation time.
    """
    fr = spikemonitor.count/sim_time
    return fr

def isi_mean_std(spikemonitor):
    """ Calculate the ISI distribution, its
        mean and its standard deviation.
        Useful to calculate CV. 
    """
    trains = spikemonitor.spike_trains()
    i = ran.randint(0,len(trains)-1)
    train = trains[i]
    if train.size == 0.:
        isi = "not firing"
        mean_isi = "not firing"
        std_isi = "not firing"
    else:
        isi = np.diff(train)
        mean_isi = np.mean(isi)
        std_isi = np.std(isi)
    return isi, mean_isi, std_isi

def variance_time_fluctuations_v(stmonit):
    """Mi serve per calcolare 
    """
    mean_v_pop = np.mean(stmonit.v, 0)
    sigma_2v = np.mean(mean_v_pop**2) - (np.mean(mean_v_pop))**2
    return sigma_2v

def variance_time_flu_v_norm(N_neur, stmonit):
    sigma_2v_tot = 0
    for i in range(N_neur):
        sigma_2v = np.mean(stmonit.v[i]**2) - (np.mean(stmonit.v[i]))**2
        sigma_2v_tot += sigma_2v
    norm = sigma_2v_tot / N_neur
    return norm

def coeffvar(stdisi, meanisi):
    if meanisi == "not firing":
        cv = float('nan')
    else:
        cv = stdisi/meanisi
    return cv