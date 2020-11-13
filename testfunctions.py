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

def firingrate2(sim_time, num_pop, count_funct):
    """ Roba molto convoluta, la tengo solo per modificarla in seguito
    """
    delta_time = 100.*ms
    time_intervals = sim_time/delta_time
    int_time_inter = int(time_intervals)
    range_of_sim = range(int_time_inter)
    spikes_per_intervals = np.zeros(num_pop)
    for trial in range_of_sim:
        restore()
        run(delta_time)
        spikes_for_neurons = []
        for neuron in range(num_pop):
            spikes_for_neurons.append(count_funct[neuron])
        spikes_for_neurons = np.asarray(spikes_for_neurons)
        spikes_per_intervals = np.vstack((spikes_per_intervals, spikes_for_neurons))
        store()
    spikes_per_intervals = np.delete(spikes_per_intervals, 0, 0)
    frequencies_per_intervals = spikes_per_intervals/(duration/100.)
    return frequencies_per_intervals, spikes_per_intervals

def firingrate(spikemonitor, sim_time):
    """ Calculte the firing rate over the
        entire simulation time.
    """
    fr = spikemonitor.count/sim_time
    return fr

def isi_mean_std(spikemonitor, whichneuron):
    """ Calculate the ISI distribution, its
        mean and its standard deviation.
        Useful to calculate CV. 
    """
    spiketrains = spikemonitor.spike_trains()
    isi = []
    x = whichneuron
    for y in range(1, len(spiketrains[x])):
        z = spiketrains[x][y] - spiketrains[x][y-1]
        isi.append(z)
    isi = np.asarray(isi)*second
    mean_isi = np.mean(isi)
    std_isi = np.std(isi)
    return mean_isi, std_isi

def printpoprate(title, poprates, colors):
    """ This plots some Population Rates.
        Input: poprates and colors are lists, for each poprate
        in poprates a color in colors is associated.
    """
    plt.figure("Pop Rate")
    plt.title(title)
    plt.ylabel("Firing Rate (Hz)")
    plt.xlabel("Time (ms)")
    for poprate, color in zip(poprates, colors):
        plt.plot(t_recorded/ms, poprate/Hz, color)
    

def printcurrents(figure, title, currents, colors):
    """ Plots the mean excitatory and inhibitory
        currents in my loops.
    """
    plt.figure(figure)
    plt.title(title)
    plt.ylabel("Currents (pA)")
    plt.xlabel("Time (ms)")
    for current, color in zip(currents, colors):
        plt.plot(t_recorded/ms, current/pamp, color)
    


def printpotential(title, statemonitors, colors, whichneuron):
    """ Let you choose for which neuron it should plot
        its membrane potential during the simulation.
    """
    plt.figure("Membrane potential")
    plt.title(title)
    plt.ylabel("Neuron membrane voltage")
    plt.xlabel("Time (ms)")
    for statemonitor, color in zip(statemonitors, colors):
        plt.plot(t_recorded/ms, statemonitor.v[whichneuron]/mV, color)


def printspikes(title, spikemonitors, colors):
    """ Plots the Raster Plot of a specific population
    """
    plt.figure("Spikes")
    plt.title(title)
    plt.ylabel("Neuron Index")
    plt.xlabel("Time (ms)")
    for spikemonitor, color in zip(spikemonitors, colors):
        plt.plot(spikemonitor.t/ms, spikemonitor.i, color, ms='2')

def variance_time_fluctuations_v(stmonit):
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

def variance_time_fluctuations_v_3pop(stmonit1, stmonit2, stmonit3):
    v_pop = stmonit1.v
    v_pop = np.vstack((v_pop, stmonit2.v))
    v_pop = np.vstack((v_pop, stmonit3.v))
    mean_v_pop = np.mean(v_pop, 0)
    sigma_2v = np.mean(mean_v_pop**2) - (np.mean(mean_v_pop))**2
    return sigma_2v

def variance_time_flu_v_norm_3pop(N_neurs, stmonits):
    sigma_2v_tot = 0
    for j in range(3):
        for i in range(N_neurs[j]):
            sigma_2v = np.mean(stmonits[j].v[i]**2) - (np.mean(stmonits[j].v[i]))**2
            sigma_2v_tot += sigma_2v
    N_3pop = 0
    for N_neur in N_neurs:
        N_3pop += N_neur
    norm = sigma_2v_tot / N_3pop
    return norm