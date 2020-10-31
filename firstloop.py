""" This is the code needed to simulate
    the GPe-STN Loop. Here I'm using the
    Brian2 framework.
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

""" The model proposed is inspired by Izhikevich 2003/2007a,
    and it has been modified by Z. Fountas for a take on Action Selection modelling.
"""

""" All the populations' NeuronGroup, first the STN ones and then the GPe ones and finally
    the Cortical Poisson Group
"""
STNRBGroup = b2.NeuronGroup(N_STN_RB, eqs_STN_RB, threshold='v>v_peak_STN_RB+U*u2', 
reset='v=cSTN_RB-U*u2;u1=u1+dSTN1_RB;u2=u2+dSTN2_RB', method='euler')

STNLLRSGroup = b2.NeuronGroup(N_STN_LLRS, eqs_STN_LLRS, threshold='v>v_peak_STN_LLRS+U*u2', 
reset='v=cSTN_LLRS-U*u2;u1=u1+dSTN1_LLRS;u2=u2+dSTN2_LLRS', method='euler')

STNNRGroup = b2.NeuronGroup(N_STN_NR, eqs_STN_NR, threshold='v>v_peak_STN_NR+U*u2', 
reset='v=cSTN_NR-U*u2;u1=u1+dSTN1_NR;u2=u2+dSTN2_NR', method='euler')

GPeAGroup = b2.NeuronGroup(N_GPe_A, eqs_GPe_A, threshold='v>v_peak_GPe_A', reset='v=cGPe_A;u=u+dGPe_A', method='euler')

GPeBGroup = b2.NeuronGroup(N_GPe_B, eqs_GPe_B, threshold='v>v_peak_GPe_B', reset='v=cGPe_B;u=u+dGPe_B', method='euler')

GPeCGroup = b2.NeuronGroup(N_GPe_C, eqs_GPe_C, threshold='v>v_peak_GPe_C', reset='v=cGPe_C;u=u+dGPe_C', method='euler')

CorticalGroup = b2.PoissonGroup(N_input, rates='input_rates(t)')

# g is the synapses' efficacy
g = 0.001

""" Cortex to STN synapse
"""
ChemicalCTXSTNRB = b2.Synapses(CorticalGroup, STNRBGroup, delay=lambda_ctx_stn, 
on_pre="gsyn_ampa_ctx_stn+=g;gsyn_nmda_ctx_stn+=g")
ChemicalCTXSTNRB.connect(True, p=p_CTX_STN)

ChemicalCTXSTNLLRS = b2.Synapses(CorticalGroup, STNLLRSGroup, delay=lambda_ctx_stn, 
on_pre="gsyn_ampa_ctx_stn+=g;gsyn_nmda_ctx_stn+=g")
ChemicalCTXSTNLLRS.connect(True, p=p_CTX_STN)

ChemicalCTXSTNNR = b2.Synapses(CorticalGroup, STNNRGroup, delay=lambda_ctx_stn, 
on_pre="gsyn_ampa_ctx_stn+=g;gsyn_nmda_ctx_stn+=g")
ChemicalCTXSTNNR.connect(True, p=p_CTX_STN)


""" GPe to GPe synapses
"""
# Self connections
ChemicalGPeAGPeA = b2.Synapses(GPeAGroup, GPeAGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeAGPeA.connect(True, p=p_GPe_GPe)

ChemicalGPeBGPeB = b2.Synapses(GPeBGroup, GPeBGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeBGPeB.connect(True, p=p_GPe_GPe)

ChemicalGPeCGPeC = b2.Synapses(GPeCGroup, GPeCGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeCGPeC.connect(True, p=p_GPe_GPe)

# A to others
ChemicalGPeAGPeB = b2.Synapses(GPeAGroup, GPeBGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeAGPeB.connect(True, p=p_GPe_GPe)

ChemicalGPeAGPeC = b2.Synapses(GPeAGroup, GPeCGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeAGPeC.connect(True, p=p_GPe_GPe)

# B to others
ChemicalGPeBGPeC = b2.Synapses(GPeBGroup, GPeCGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeBGPeC.connect(True, p=p_GPe_GPe)

ChemicalGPeBGPeA = b2.Synapses(GPeBGroup, GPeAGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeBGPeA.connect(True, p=p_GPe_GPe)

# C to others
ChemicalGPeCGPeA = b2.Synapses(GPeCGroup, GPeAGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeCGPeA.connect(True, p=p_GPe_GPe)

ChemicalGPeCGPeB = b2.Synapses(GPeCGroup, GPeBGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeCGPeB.connect(True, p=p_GPe_GPe)


""" GPe to STN synapses
"""
# A to RB/LLRS/NR
ChemicalGPeASTNRB = b2.Synapses(GPeAGroup, STNRBGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeASTNRB.connect(True, p=p_GPe_STN)

ChemicalGPeASTNLLRS = b2.Synapses(GPeAGroup, STNLLRSGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeASTNLLRS.connect(True, p=p_GPe_STN)

ChemicalGPeASTNNR = b2.Synapses(GPeAGroup, STNNRGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeASTNNR.connect(True, p=p_GPe_STN)

# B to RB/LLRS/NR
ChemicalGPeBSTNRB = b2.Synapses(GPeBGroup, STNRBGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeBSTNRB.connect(True, p=p_GPe_STN)

ChemicalGPeBSTNLLRS = b2.Synapses(GPeBGroup, STNLLRSGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeBSTNLLRS.connect(True, p=p_GPe_STN)

ChemicalGPeBSTNNR = b2.Synapses(GPeBGroup, STNNRGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeBSTNNR.connect(True, p=p_GPe_STN)

# C to RB/LLRS/NR
ChemicalGPeCSTNRB = b2.Synapses(GPeCGroup, STNRBGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeCSTNRB.connect(True, p=p_GPe_STN)

ChemicalGPeCSTNLLRS = b2.Synapses(GPeCGroup, STNLLRSGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeCSTNLLRS.connect(True, p=p_GPe_STN)

ChemicalGPeCSTNNR = b2.Synapses(GPeCGroup, STNNRGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeCSTNNR.connect(True, p=p_GPe_STN)


""" STN to GPe synapses
"""
# RB to A/B/C
ChemicalSTNRBGPeA = b2.Synapses(STNRBGroup, GPeAGroup,delay=lambda_stn_gpe, model='w:volt',
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNRBGPeA.connect(True, p=p_STN_GPe)

ChemicalSTNRBGPeB = b2.Synapses(STNRBGroup, GPeBGroup,delay=lambda_stn_gpe, model='w:volt',  
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNRBGPeB.connect(True, p=p_STN_GPe)

ChemicalSTNRBGPeC = b2.Synapses(STNRBGroup, GPeCGroup,delay=lambda_stn_gpe, model='w:volt', 
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNRBGPeC.connect(True, p=p_STN_GPe)

# LLRS to A/B/C
ChemicalSTNLLRSGPeA = b2.Synapses(STNLLRSGroup, GPeAGroup,delay=lambda_stn_gpe, model='w:volt', 
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNLLRSGPeA.connect(True, p=p_STN_GPe)

ChemicalSTNLLRSGPeB = b2.Synapses(STNLLRSGroup, GPeBGroup,delay=lambda_stn_gpe, model='w:volt', 
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNLLRSGPeB.connect(True, p=p_STN_GPe)

ChemicalSTNLLRSGPeC = b2.Synapses(STNLLRSGroup, GPeCGroup,delay=lambda_stn_gpe, model='w:volt', 
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNLLRSGPeC.connect(True, p=p_STN_GPe)

# NR to A/B/C
ChemicalSTNNRGPeA = b2.Synapses(STNNRGroup, GPeAGroup,delay=lambda_stn_gpe, model='w:volt', 
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNNRGPeA.connect(True, p=p_STN_GPe)

ChemicalSTNNRGPeB = b2.Synapses(STNNRGroup, GPeBGroup,delay=lambda_stn_gpe, model='w:volt', 
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNNRGPeB.connect(True, p=p_STN_GPe)

ChemicalSTNNRGPeC = b2.Synapses(STNNRGroup, GPeCGroup,delay=lambda_stn_gpe, model='w:volt', 
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNNRGPeC.connect(True, p=p_STN_GPe)


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

b2.plt.figure("Eheh")
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