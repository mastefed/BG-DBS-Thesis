""" This is the code needed to simulate
    the GPe-STN Loop. Here I'm using the
    Brian2 framework.

    The model proposed is inspired by Izhikevich 2003/2007a,
    and it has been modified by Z. Fountas for a take on Action Selection modelling.
"""

""" T = [26.31; 83.33] secondi
    oscillazioni nella frequenza beta
"""

from brian2 import *
import random as ran
import numpy as np
from scipy.signal import butter, welch, filtfilt
from scipy.integrate import simps
from parameters import *
from equations import *
from groupsandsynapses import *
from testfunctions import *

run(300*ms)

""" Functions to monitor neurons' state
"""
spikemonitorSTNRB = SpikeMonitor(STNRBGroup, variables=['v'])
statemonitorSTNRB = StateMonitor(STNRBGroup, ['v','I_lfp_stnrb'], record=True)

spikemonitorSTNLLRS = SpikeMonitor(STNLLRSGroup, variables=['v'])
statemonitorSTNLLRS = StateMonitor(STNLLRSGroup, ['v','I_lfp_stnllrs'], record=True)

spikemonitorSTNNR = SpikeMonitor(STNNRGroup, variables=['v'])
statemonitorSTNNR = StateMonitor(STNNRGroup, ['v','I_lfp_stnnr'], record=True)

spikemonitorGPeA = SpikeMonitor(GPeAGroup, variables=['v'])
statemonitorGPeA = StateMonitor(GPeAGroup, ['v','I_lfp_gpea'], record=True)

spikemonitorGPeB = SpikeMonitor(GPeBGroup, variables=['v'])
statemonitorGPeB = StateMonitor(GPeBGroup, ['v','I_lfp_gpeb'], record=True)

spikemonitorGPeC = SpikeMonitor(GPeCGroup, variables=['v'])
statemonitorGPeC = StateMonitor(GPeCGroup, ['v','I_lfp_gpec'], record=True)

spikemonitorCTX = SpikeMonitor(CorticalGroup)

populationSTNRB = PopulationRateMonitor(STNRBGroup)
populationSTNLLRS = PopulationRateMonitor(STNLLRSGroup)
populationSTNNR = PopulationRateMonitor(STNNRGroup)

populationGPeA = PopulationRateMonitor(GPeAGroup)
populationGPeB = PopulationRateMonitor(GPeBGroup)
populationGPeC = PopulationRateMonitor(GPeCGroup)

run(duration) # Run boy, run!

""" Calculating the Firing Rates for the entire simulation
"""
frGPeA = firingrate(spikemonitorGPeA, duration)
frGPeB = firingrate(spikemonitorGPeB, duration)
frGPeC = firingrate(spikemonitorGPeC, duration)
frSTNRB = firingrate(spikemonitorSTNRB, duration)
frSTNLLRS = firingrate(spikemonitorSTNLLRS, duration)
frSTNNR = firingrate(spikemonitorSTNNR, duration)
frCTX = firingrate(spikemonitorCTX, duration)

print(f"La frequenza f dell'input rate della CTX è: {input_rates(416*ms)}\n")
print(f"Il firing rate della CTX è: {np.mean(frCTX)} Hz\n")
print(f"Il firing rate del GPe A è: {np.mean(frGPeA)} Hz\n")
print(f"Il firing rate del GPe B è: {np.mean(frGPeB)} Hz\n")
print(f"Il firing rate del GPe C è: {np.mean(frGPeC)} Hz\n")
print(f"Il firing rate del STN RB è: {np.mean(frSTNRB)} Hz\n")
print(f"Il firing rate del STN LLRS è: {np.mean(frSTNLLRS)} Hz\n")
print(f"Il firing rate del STN NR è: {np.mean(frSTNNR)} Hz\n")

mean_isiGPeA, std_isiGPeA = isi_mean_std(spikemonitorGPeA, 0)
mean_isiGPeB, std_isiGPeB = isi_mean_std(spikemonitorGPeB, 2)
mean_isiGPeC, std_isiGPeC = isi_mean_std(spikemonitorGPeC, 1)
mean_isiSTNRB, std_isiSTNRB = isi_mean_std(spikemonitorSTNRB, 3)
mean_isiSTNLLRS, std_isiSTNLLRS = isi_mean_std(spikemonitorSTNLLRS, 0)
mean_isiSTNNR, std_isiSTNNR = isi_mean_std(spikemonitorSTNNR, 1)

print("Il coefficiente di variazione (in percentuale) per ISI per un neurone di:\n")
print(f"GPe A {std_isiGPeA/mean_isiGPeA}\n")
print(f"GPe B {std_isiGPeB/mean_isiGPeB}\n")
print(f"GPe C {std_isiGPeC/mean_isiGPeC}\n")
print(f"STN RB {std_isiSTNRB/mean_isiSTNRB}\n")
print(f"STN LLRS {std_isiSTNLLRS/mean_isiSTNLLRS}\n")
print(f"STN NR {std_isiSTNNR/mean_isiSTNNR}\n")

""" Calculating the Population firing rate over time for STN and GPe
"""
width = 2.*ms
populationSTNfr = np.mean([populationSTNRB.smooth_rate(width=width), populationSTNNR.smooth_rate(width=width), populationSTNLLRS.smooth_rate(width=width)], 0)
populationGPefr = np.mean([populationGPeA.smooth_rate(width=width), populationGPeB.smooth_rate(width=width), populationGPeC.smooth_rate(width=width)], 0)

""" Calculating meaning currents: mean excitatory and inhibitory current and mean currents to STN and GPe
"""
# Qua calcolare LFP e poi Welch nelle bande spettrali
mean_I_lfp_STNRB = np.mean(statemonitorSTNRB.I_lfp_stnrb, 0)
mean_I_lfp_STNLLRS = np.mean(statemonitorSTNLLRS.I_lfp_stnllrs, 0)
mean_I_lfp_STNNR = np.mean(statemonitorSTNNR.I_lfp_stnnr, 0)
mean_I_lfp_GPeA = np.mean(statemonitorGPeA.I_lfp_gpea, 0)
mean_I_lfp_GPeB = np.mean(statemonitorGPeB.I_lfp_gpeb, 0)
mean_I_lfp_GPeC = np.mean(statemonitorGPeC.I_lfp_gpec, 0)

mean_I_lfp_STN = np.vstack((mean_I_lfp_STNRB, mean_I_lfp_STNLLRS, mean_I_lfp_STNNR))
mean_I_lfp_STN = np.mean(mean_I_lfp_STN, 0)
mean_I_lfp_GPe = np.vstack((mean_I_lfp_GPeA, mean_I_lfp_GPeB, mean_I_lfp_GPeC))
mean_I_lfp_GPe = np.mean(mean_I_lfp_GPe, 0)

filtered_lfp_STN = butter_bandpass_filter(mean_I_lfp_STN, 1, 100, 1/deft, order=3)
filtered_lfp_GPe = butter_bandpass_filter(mean_I_lfp_GPe, 1, 100, 1/deft, order=3)

printcurrents(3, "LFP STN (red) GPe (green)", [filtered_lfp_STN, filtered_lfp_GPe], ['r', 'g'])

f1, specstn = welch(filtered_lfp_STN, fs=1/deft, nperseg=2/deft)
f2, specgpe = welch(filtered_lfp_GPe, fs=1/deft, nperseg=2/deft)
low = 12*Hz
high = 38*Hz
idx_beta1 = np.logical_and(f1 >= low, f1 <= high)
idx_beta2 = np.logical_and(f2 >= low, f2 <= high)

print(f1[1])
print(f1[0])

"""
plt.figure(5)
plt.title("Spectral density LFP STN (green) LFP GPe (red)")
plt.xlabel("Frequencies (Hz)")
plt.xlim(0,150)
plt.fill_between(f1, specstn, where=idx_beta1, color='c')
plt.fill_between(f2, specgpe, where=idx_beta2, color='m')
plt.plot(f2, specgpe, 'r')
plt.plot(f1, specstn, 'g')
"""
plt.show()