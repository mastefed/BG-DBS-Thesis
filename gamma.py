from brian2 import *
import matplotlib.pyplot as plt

N = 5000
N_inhi = 1000
N_exci = 4000
duration = 500*ms

p = 0.2 # connectivity probability

v_rest = 0*mV # resting potential
v_thre = 18*mV # threshold potential
v_rese = 11*mV # reset potential

tr_inhi = 1*ms # refractory time for inhibitory group
tr_exci = 2*ms # refractory time for excitatory group

tm_inhi = 10*ms # time costant for inhibitory group
tm_exci = 20*ms # time costant for excitatory group

tda_inhi = 1*ms # decay time for ampa current into inhi neuron
tda_exci = 2*ms # decay time for ampa current into exci neuron
tra_inhi = 0.2*ms # rise time for ampa current into inhi neuron
tra_exci = 0.4*ms # rise time for ampa current into exci neuron

tl = 1*ms # latency of post-synaptic current

tdg = 5*ms # decay time of gaba current
trg = 0.25*ms # rise time of gaba current

# Synaptic efficacies int/pyr/ext to GABA
j_int_inhi = 2.7*mV
j_pyr_inhi = 0.7*mV
j_ext_inhi = 0.95*mV

# Synaptic efficacies int/pyr/ext to AMPA
j_int_exci = 1.7*mV
j_pyr_exci = 0.42*mV
j_ext_exci = 0.55*mV

# Non ho ancora messo le delta di dirac

eqs_inhi = '''
dv/dt = 1/tm_inhi * (-v + I_a - I_g) : volt (unless refractory)
dI_a/dt = 1/tda_inhi * (-I_a + X_a) : amp
dX_a/dt = 1/tra_inhi * (-X_a + tm_inhi*(j_pyr_inhi + j_ext_inhi)) : weber
dI_g/dt = 1/tdg * (-I_g + X_g) : 1
dX_g/dt = 1/trg * (-X_g + tm_inhi*(j_int_inhi)) : 1
'''

# Non ho ancora messo le delta di dirac

eqs_exci = '''
dv/dt = 1/tm_exci * (-v + I_a - I_g) : volt (unless refractory)
dI_a/dt = 1/tda_exci * (-I_a + X_a) : 1
dX_a/dt = 1/tra_exci * (-X_a + tm_exci*(j_pyr_exci + j_ext_exci)) : 1
dI_g/dt = 1/tdg * (-I_g + X_g) : 1
dX_g/dt = 1/trg * (-X_g + tm_exci*(j_int_exci)) : 1
'''

I = NeuronGroup(N_inhi, eqs_inhi, threshold='v>v_thre', reset='v=v_rese',
                    refractory=tr_inhi, method='exact')

E = NeuronGroup(N_exci, eqs_exci, threshold='v>v_thre', reset='v=v_rese',
                    refractory=tr_exci, method='exact')



M_inhi = SpikeMonitor(I)
M_exci = SpikeMonitor(E)
run(duration)
