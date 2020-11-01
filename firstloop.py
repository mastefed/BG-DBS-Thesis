""" 
    This is the code needed to simulate
    the GPe-STN Loop. Here I'm using the
    Brian2 framework.

    The model proposed is inspired by Izhikevich 2003/2007a,
    and it has been modified by Z. Fountas for a take on Action Selection modelling.
"""

""" Functions I'll need later in the code
"""
def firingrate(sim_time, num_pop, count_funct):
    time_intervals = sim_time/(100.*b2.ms)
    int_time_inter = int(time_intervals)
    range_of_sim = range(int_time_inter)
    spikes_per_intervals = np.zeros(num_pop)
    for trial in range_of_sim:
        b2.restore()
        b2.run(sim_time/100.)
        spikes_for_neurons = []
        for neuron in range(num_pop):
            spikes_for_neurons.append(count_funct[neuron])
        spikes_for_neurons = np.asarray(spikes_for_neurons)
        spikes_per_intervals = np.vstack((spikes_per_intervals, spikes_for_neurons))
        #print(str(trial)+" trial done!")
        b2.store()
    spikes_per_intervals = np.delete(spikes_per_intervals, 0, 0)
    frequencies_per_intervals = spikes_per_intervals/(duration/100.)
    return frequencies_per_intervals, spikes_per_intervals

import brian2 as b2
import random as ran
import numpy as np
from scipy import signal
from parameters import *
from equations import *
from groupsandsynapses import *


""" Functions to monitor neurons' state
"""
spikemonitorSTNRB = b2.SpikeMonitor(STNRBGroup, variables=['v'])
statemonitorSTNRB = b2.StateMonitor(STNRBGroup, ['v','I_syn_tot','I_chem_CTX_STN','I_chem_GPe_STN'], record=True)

spikemonitorSTNLLRS = b2.SpikeMonitor(STNLLRSGroup, variables=['v'])
statemonitorSTNLLRS = b2.StateMonitor(STNLLRSGroup, ['v','I_syn_tot','I_chem_CTX_STN','I_chem_GPe_STN'], record=True)

spikemonitorSTNNR = b2.SpikeMonitor(STNNRGroup, variables=['v'])
statemonitorSTNNR = b2.StateMonitor(STNNRGroup, ['v','I_syn_tot','I_chem_CTX_STN','I_chem_GPe_STN'], record=True)

spikemonitorGPeA = b2.SpikeMonitor(GPeAGroup, variables=['v'])
statemonitorGPeA = b2.StateMonitor(GPeAGroup, ['v','I_syn_tot','I_chem_STN_GPe','I_chem_GPe_GPe'], record=True)

spikemonitorGPeB = b2.SpikeMonitor(GPeBGroup, variables=['v'])
statemonitorGPeB = b2.StateMonitor(GPeBGroup, ['v','I_syn_tot','I_chem_STN_GPe','I_chem_GPe_GPe'], record=True)

spikemonitorGPeC = b2.SpikeMonitor(GPeCGroup, variables=['v'])
statemonitorGPeC = b2.StateMonitor(GPeCGroup, ['v','I_syn_tot','I_chem_STN_GPe','I_chem_GPe_GPe'], record=True)

spikemonitorCTX = b2.SpikeMonitor(CorticalGroup)

populationSTNRB = b2.PopulationRateMonitor(STNRBGroup)
populationSTNLLRS = b2.PopulationRateMonitor(STNLLRSGroup)
populationSTNNR = b2.PopulationRateMonitor(STNNRGroup)

populationGPeA = b2.PopulationRateMonitor(GPeAGroup)
populationGPeB = b2.PopulationRateMonitor(GPeBGroup)
populationGPeC = b2.PopulationRateMonitor(GPeCGroup)

b2.store()

######################
""" Run the code!
"""
#b2.run(duration)
######################

countGPeA = spikemonitorGPeA.count
countGPeB = spikemonitorGPeB.count
countGPeC = spikemonitorGPeC.count
countSTNRB = spikemonitorSTNRB.count
countSTNLLRS = spikemonitorSTNLLRS.count
countSTNNR = spikemonitorSTNNR.count
countCTX = spikemonitorCTX.count

# Firing rate calculated of 100 ms intervals
firingrateGPeA, spikesGPeA = firingrate(duration, N_GPe_A, countGPeA) # occhio, qui dentro si annidano dei store(), restore()
firingrateGPeB, spikesGPeB = firingrate(duration, N_GPe_B, countGPeB) 
firingrateGPeC, spikesGPeC = firingrate(duration, N_GPe_C, countGPeC) 
firingrateSTNRB, spikesSTNRB = firingrate(duration, N_STN_RB, countSTNRB)
firingrateSTNLLRS, spikesSTNLLRS = firingrate(duration, N_STN_LLRS, countSTNLLRS)
firingrateSTNNR, spikesSTNNR = firingrate(duration, N_STN_NR, countSTNNR)

mean_over_intervals_fr_GPeA = np.mean(firingrateGPeA, 0)
mean_over_intervals_fr_GPeB = np.mean(firingrateGPeB, 0)
mean_over_intervals_fr_GPeC = np.mean(firingrateGPeC, 0)
mean_over_intervals_fr_STNRB = np.mean(firingrateSTNRB, 0)
mean_over_intervals_fr_STNLLRS = np.mean(firingrateSTNLLRS, 0)
mean_over_intervals_fr_STNNR = np.mean(firingrateSTNNR, 0)

b2.plt.figure("Mean firing rate over 100 milliseconds")
b2.plt.title("Mean firing rate of GPe B neurons")
b2.plt.ylabel("Counts")
b2.plt.xlabel("Firing rate (Hz)")
b2.plt.hist(mean_over_intervals_fr_GPeB/b2.Hz, bins='auto')

""" Calculating the Population firing rate over time for STN and GPe
"""
width = 2.*b2.ms
populationSTN1 = np.add(populationSTNRB.smooth_rate(width=width), populationSTNNR.smooth_rate(width=width))
populationSTN = np.add(populationSTN1, populationSTNNR.smooth_rate(width=width))
populationGPe1 = np.add(populationGPeA.smooth_rate(width=width), populationGPeB.smooth_rate(width=width))
populationGPe = np.add(populationGPe1, populationGPeC.smooth_rate(width=width))

""" Calculating meaning currents: mean excitatory and inhibitory current and mean currents to STN and GPe
"""
mean_I_chem_GPe_GPe = np.add(np.mean(statemonitorGPeA.I_chem_GPe_GPe,0), np.mean(statemonitorGPeB.I_chem_GPe_GPe,0), np.mean(statemonitorGPeC.I_chem_GPe_GPe,0))
mean_I_chem_CTX_STN = np.add(np.mean(statemonitorSTNRB.I_chem_CTX_STN,0), np.mean(statemonitorSTNLLRS.I_chem_CTX_STN,0), np.mean(statemonitorSTNNR.I_chem_CTX_STN,0))
mean_I_chem_STN_GPe = np.add(np.mean(statemonitorGPeA.I_chem_STN_GPe,0), np.mean(statemonitorGPeB.I_chem_STN_GPe,0), np.mean(statemonitorGPeC.I_chem_STN_GPe,0))
mean_I_chem_GPe_STN = np.add(np.mean(statemonitorSTNRB.I_chem_GPe_STN,0), np.mean(statemonitorSTNLLRS.I_chem_GPe_STN,0), np.mean(statemonitorSTNNR.I_chem_GPe_STN,0))

mean_I_exci = np.add(mean_I_chem_CTX_STN,mean_I_chem_STN_GPe)
mean_I_inhi = np.add(mean_I_chem_GPe_GPe,mean_I_chem_GPe_STN)

mean_I_to_STNRB = np.mean(statemonitorSTNRB.I_syn_tot, 0)
mean_I_to_STNLLRS = np.mean(statemonitorSTNLLRS.I_syn_tot, 0)
mean_I_to_STNNR = np.mean(statemonitorSTNNR.I_syn_tot, 0)
mean_I_to_GPeA = np.mean(statemonitorGPeA.I_syn_tot, 0)
mean_I_to_GPeB = np.mean(statemonitorGPeB.I_syn_tot, 0)
mean_I_to_GPeC = np.mean(statemonitorGPeC.I_syn_tot, 0)

tot_curr_to_STN = np.add(mean_I_to_STNRB, mean_I_to_STNNR, mean_I_to_STNLLRS)
tot_curr_to_GPe = np.add(mean_I_to_GPeA, mean_I_to_GPeB, mean_I_to_GPeC)


b2.plt.show()

""" T = [26.31; 83.33] secondi
oscillazioni nella frequenza beta
"""