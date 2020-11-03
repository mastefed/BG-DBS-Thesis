""" 
    This is the code needed to simulate
    the GPe-STN Loop. Here I'm using the
    Brian2 framework.

    The model proposed is inspired by Izhikevich 2003/2007a,
    and it has been modified by Z. Fountas for a take on Action Selection modelling.
"""

""" 
    T = [26.31; 83.33] secondi
    oscillazioni nella frequenza beta
"""

""" 
    Functions I'll need later in the code
"""
def firingrate(sim_time, num_pop, count_funct):
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
        #print(str(trial)+" trial done!")
        store()
    spikes_per_intervals = np.delete(spikes_per_intervals, 0, 0)
    frequencies_per_intervals = spikes_per_intervals/(duration/100.)
    return frequencies_per_intervals, spikes_per_intervals

from brian2 import *
import random as ran
import numpy as np
from scipy import signal
from parameters import *
from equations import *
from groupsandsynapses import *

""" Functions to monitor neurons' state
"""
spikemonitorSTNRB = SpikeMonitor(STNRBGroup, variables=['v'])
statemonitorSTNRB = StateMonitor(STNRBGroup, ['v','I_syn_tot','I_chem_CTX_STN','I_chem_GPe_STN'], record=True)

spikemonitorSTNLLRS = SpikeMonitor(STNLLRSGroup, variables=['v'])
statemonitorSTNLLRS = StateMonitor(STNLLRSGroup, ['v','I_syn_tot','I_chem_CTX_STN','I_chem_GPe_STN'], record=True)

spikemonitorSTNNR = SpikeMonitor(STNNRGroup, variables=['v'])
statemonitorSTNNR = StateMonitor(STNNRGroup, ['v','I_syn_tot','I_chem_CTX_STN','I_chem_GPe_STN'], record=True)

spikemonitorGPeA = SpikeMonitor(GPeAGroup, variables=['v'])
statemonitorGPeA = StateMonitor(GPeAGroup, ['v','I_syn_tot','I_chem_STN_GPe','I_chem_GPe_GPe'], record=True)

spikemonitorGPeB = SpikeMonitor(GPeBGroup, variables=['v'])
statemonitorGPeB = StateMonitor(GPeBGroup, ['v','I_syn_tot','I_chem_STN_GPe','I_chem_GPe_GPe'], record=True)

spikemonitorGPeC = SpikeMonitor(GPeCGroup, variables=['v'])
statemonitorGPeC = StateMonitor(GPeCGroup, ['v','I_syn_tot','I_chem_STN_GPe','I_chem_GPe_GPe'], record=True)

spikemonitorCTX = SpikeMonitor(CorticalGroup)

populationSTNRB = PopulationRateMonitor(STNRBGroup)
populationSTNLLRS = PopulationRateMonitor(STNLLRSGroup)
populationSTNNR = PopulationRateMonitor(STNNRGroup)

populationGPeA = PopulationRateMonitor(GPeAGroup)
populationGPeB = PopulationRateMonitor(GPeBGroup)
populationGPeC = PopulationRateMonitor(GPeCGroup)

run(duration)

countGPeA = spikemonitorGPeA.count/duration
countGPeB = spikemonitorGPeB.count/duration
countGPeC = spikemonitorGPeC.count/duration
countSTNRB = spikemonitorSTNRB.count/duration
countSTNLLRS = spikemonitorSTNLLRS.count/duration
countSTNNR = spikemonitorSTNNR.count/duration
countCTX = spikemonitorCTX.count/duration

print("Il firing rate del GPe A è:")
print(countGPeA)
print("Il firing rate del GPe B è:")
print(countGPeB)
print("Il firing rate del GPe C è:")
print(countGPeC)
print("Il firing rate del STN RB è:")
print(countSTNRB)
print("Il firing rate del STN LLRS è:")
print(countSTNLLRS)
print("Il firing rate del STN NR è:")
print(countSTNNR)


"""
# Firing rate calculated of 100 ms intervals
firingrateGPeA, spikesGPeA = firingrate(duration, N_GPe_A, countGPeA) # occhio, qui dentro si annidano degli store(), restore()
firingrateGPeB, spikesGPeB = firingrate(duration, N_GPe_B, countGPeB) 
firingrateGPeC, spikesGPeC = firingrate(duration, N_GPe_C, countGPeC) 
firingrateSTNRB, spikesSTNRB = firingrate(duration, N_STN_RB, countSTNRB)
firingrateSTNLLRS, spikesSTNLLRS = firingrate(duration, N_STN_LLRS, countSTNLLRS)
firingrateSTNNR, spikesSTNNR = firingrate(duration, N_STN_NR, countSTNNR)
firingrateCTX, spikesCTX = firingrate(duration, N_input, countCTX)

mean_over_intervals_fr_GPeA = np.mean(firingrateGPeA, 0)
mean_over_intervals_fr_GPeB = np.mean(firingrateGPeB, 0)
mean_over_intervals_fr_GPeC = np.mean(firingrateGPeC, 0)
mean_over_intervals_fr_STNRB = np.mean(firingrateSTNRB, 0)
mean_over_intervals_fr_STNLLRS = np.mean(firingrateSTNLLRS, 0)
mean_over_intervals_fr_STNNR = np.mean(firingrateSTNNR, 0)
mean_over_intervals_fr_CTX = np.mean(firingrateCTX, 0)

plt.figure("Mean firing rate over 100 milliseconds")
plt.title("Mean firing rate of GPe A neurons")
plt.ylabel("Counts")
plt.xlabel("Firing rate (Hz)")
plt.hist(mean_over_intervals_fr_GPeA/Hz, bins='auto')

plt.figure("Mean firing rate over 100 milliseconds")
plt.title("Mean firing rate of GPe B neurons")
plt.ylabel("Counts")
plt.xlabel("Firing rate (Hz)")
plt.hist(mean_over_intervals_fr_GPeB/Hz, bins='auto')

plt.figure("Mean firing rate over 100 milliseconds")
plt.title("Mean firing rate of GPe C neurons")
plt.ylabel("Counts")
plt.xlabel("Firing rate (Hz)")
plt.hist(mean_over_intervals_fr_GPeC/Hz, bins='auto')
"""


""" Calculating the Population firing rate over time for STN and GPe
"""
width = 2.*ms
populationSTN = np.mean([populationSTNRB.smooth_rate(width=width), populationSTNNR.smooth_rate(width=width), populationSTNLLRS.smooth_rate(width=width)], 0)
populationGPe = np.mean([populationGPeA.smooth_rate(width=width), populationGPeB.smooth_rate(width=width), populationGPeC.smooth_rate(width=width)], 0)

'''
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
'''

############################
# I like to print stuff

plt.figure("Pop Rate")
plt.title("Population firing rate for STN (green) and GPe (blue) populations ")
plt.ylabel("Firing Rate (Hz)")
plt.xlabel("Time (ms)")
plt.plot(populationSTNRB.t/ms, populationSTN/Hz, 'g')
plt.plot(populationGPeB.t/ms, populationGPe/Hz, 'b')

'''
""" Plotting Excitatory and Inhibitory currents in my loop
"""
plt.figure("Exci-Inhi")
plt.title("Excitatory (green) and Inhibitory (red) Currents in the STN-GPe loop")
plt.ylabel("Currents (pA)")
plt.xlabel("Time (ms)")
plotExciCurrent = plt.plot(statemonitorGPeB.t/ms,mean_I_exci/pamp, 'g')
plotInhiCurrent = plt.plot(statemonitorGPeB.t/ms,mean_I_inhi/pamp, 'r')

plt.figure("Currents in STN and GPe")
plt.title("Currents arriving at STN (green) and GPe (blue)")
plt.ylabel("Currents (pA)")
plt.xlabel("Time (ms)")
plotExciCurrent = plt.plot(statemonitorGPeB.t/ms,tot_curr_to_STN/pamp, 'g')
plotInhiCurrent = plt.plot(statemonitorGPeB.t/ms,tot_curr_to_GPe/pamp, 'b')



""" Plotting STN stuff
"""
plt.figure("Membrane potential STN")
plt.title("Membrane potential of one neuron (red = STN RB) (green = STN LLRS) (blue = STN NR)")
plt.ylabel("Neuron membrane voltage")
plt.xlabel("Time (ms)")
plotSSTNNR = plt.plot(statemonitorSTNNR.t/ms, statemonitorSTNNR.v[0]/mV, 'b')
plotSSTNLLRS = plt.plot(statemonitorSTNLLRS.t/ms, statemonitorSTNLLRS.v[0]/mV, 'g')
plotSSTNRB = plt.plot(statemonitorSTNRB.t/ms, statemonitorSTNRB.v[0]/mV, 'r')


plt.figure("Spikes STN")
plt.title("Raster plot (red = STN RB) (green = STN LLRS) (blue = STN NR)")
plt.ylabel("Neuron Index")
plt.xlabel("Time (ms)")
plt.ylim((0,45))
plotMSTNRB = plt.plot(spikemonitorSTNRB.t/ms, spikemonitorSTNRB.i, 'r.',ms='2')
plotMSTNLLRS = plt.plot(spikemonitorSTNLLRS.t/ms, spikemonitorSTNLLRS.i, 'g.',ms='2')
plotMSTNNR = plt.plot(spikemonitorSTNNR.t/ms, spikemonitorSTNNR.i, 'b.',ms='2')



""" Plotting GPe stuff
"""
plt.figure("Membrane potential GPe")
plt.title("Membrane potential of one neuron (red = GPe A) (green = GPe B) (blue = GPe C)")
plt.ylabel("Neuron membrane voltage")
plt.xlabel("Time (ms)")
plotSGPeA = plt.plot(statemonitorGPeA.t/ms, statemonitorGPeA.v[0]/mV, 'r')
plotSGPeB = plt.plot(statemonitorGPeB.t/ms, statemonitorGPeB.v[0]/mV, 'g')
plotSGPeC = plt.plot(statemonitorGPeC.t/ms, statemonitorGPeC.v[0]/mV, 'b')


plt.figure("Spikes GPe")
plt.title("Raster plot (red = GPe A) (green = GPe B) (blue = GPe C)")
plt.ylabel("Neuron Index")
plt.xlabel("Time (ms)")
plt.ylim((0,153))
plotMGPeA = plt.plot(spikemonitorGPeA.t/ms, spikemonitorGPeA.i, 'r.',ms='2')
plotMGPeB = plt.plot(spikemonitorGPeB.t/ms, spikemonitorGPeB.i, 'g.',ms='2')
plotMGPeC = plt.plot(spikemonitorGPeC.t/ms, spikemonitorGPeC.i, 'b.',ms='2')
'''
plt.show()