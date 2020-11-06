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
from scipy import signal
from parameters import *
from equations import *
from groupsandsynapses import *
from testfunctions import *

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
print(f"GPe A {std_isiGPeA/mean_isiGPeA*100}%\n")
print(f"GPe B {std_isiGPeB/mean_isiGPeB*100}%\n")
print(f"GPe C {std_isiGPeC/mean_isiGPeC*100}%\n")
print(f"STN RB {std_isiSTNRB/mean_isiSTNRB*100}%\n")
print(f"STN LLRS {std_isiSTNLLRS/mean_isiSTNLLRS*100}%\n")
print(f"STN NR {std_isiSTNNR/mean_isiSTNNR*100}%\n")

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

printcurrents(1, "LFP STN RB (red) STN LLRS (green) STN NR (blue)", [mean_I_lfp_STNRB, mean_I_lfp_STNLLRS, mean_I_lfp_STNNR], ['r', 'g', 'b'])
printcurrents(2, "LFP GPe A (red) GPe B (green) GPeC (blue)", [mean_I_lfp_GPeA, mean_I_lfp_GPeB, mean_I_lfp_GPeC], ['r', 'g', 'b'])
printcurrents(3, "LFP STN (red) GPe (green)", [mean_I_lfp_STN, mean_I_lfp_GPe], ['r', 'g'])

plt.show()