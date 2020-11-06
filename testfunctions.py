""" Functions I could need in the main code
"""
from brian2 import *
from parameters import *
import numpy as np

def firingrate2(sim_time, num_pop, count_funct):
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
    fr = spikemonitor.count/sim_time
    return fr

def isi_mean_std(spikemonitor, whichneuron):
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
    """ This prints a plot of some Population Rates.
        Input: poprates and colors are lists, for each poprate
        in poprates a color in colors is associated.
    """
    plt.figure("Pop Rate")
    plt.title(title)
    plt.ylabel("Firing Rate (Hz)")
    plt.xlabel("Time (ms)")
    for poprate, color in zip(poprates, colors):
        plt.plot(t_recorded/ms, poprate/Hz, color)
    

def printexciinhicurrents(excicurrent, inhicurrent):
    plt.figure("Exci-Inhi")
    plt.title("Excitatory (green) and Inhibitory (red) Currents in the STN-GPe loop")
    plt.ylabel("Currents (pA)")
    plt.xlabel("Time (ms)")
    plt.plot(t_recorded/ms, excicurrent/pamp, 'g')
    plt.plot(t_recorded/ms, inhicurrent/pamp, 'r')
    

def printstngpecurrents(totcurrstn, totcurrgpe):
    plt.figure("Currents in STN and GPe")
    plt.title("Currents arriving at STN (green) and GPe (blue)")
    plt.ylabel("Currents (pA)")
    plt.xlabel("Time (ms)")
    plt.plot(t_recorded/ms, totcurrstn/pamp, 'g')
    plt.plot(t_recorded/ms, totcurrgpe/pamp, 'b')
    

def printpotential(title, statemonitors, colors, whichneuron):
    plt.figure("Membrane potential")
    plt.title(title)
    plt.ylabel("Neuron membrane voltage")
    plt.xlabel("Time (ms)")
    for statemonitor, color in zip(statemonitors, colors):
        plt.plot(t_recorded/ms, statemonitor.v[whichneuron]/mV, color)


def printspikes(title, spikemonitors, colors):
    plt.figure("Spikes")
    plt.title(title)
    plt.ylabel("Neuron Index")
    plt.xlabel("Time (ms)")
    for spikemonitor, color in zip(spikemonitors, colors):
        plt.plot(spikemonitor.t/ms, spikemonitor.i, color, ms='2')
