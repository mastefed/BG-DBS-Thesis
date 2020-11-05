""" Functions I could need in the main code
"""
from brian2 import *
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
