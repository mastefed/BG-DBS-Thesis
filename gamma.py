from brian2 import *
import matplotlib.pyplot as plt

N = 5000
N_inhi = 1000
N_exci = 4000
duration = 10*ms

p = 0.2 # connectivity probability
w = 1

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

# Modello le equazioni per le reti di neuroni inibitori ed eccitatori
eqs_inhi = '''
dv/dt = (-v + I_a - I_g)/tm_inhi : volt (unless refractory)
dI_a/dt = (-I_a + X_a)/tda_inhi : volt
dI_g/dt = (-I_g + X_g)/tdg : volt
X_a_tot : volt
X_g_tot : volt
'''

# La differenza me la ritrovo nelle costanti temporali
eqs_exci = '''
dv/dt = (-v + I_a - I_g)/tm_exci : volt (unless refractory)
dI_a/dt = (-I_a + X_a)/tda_exci : volt
dI_g/dt = (-I_g + X_g)/tdg : volt
X_a_tot : volt
X_g_tot : volt
'''

# Modello le equazioni per le correnti sinaptiche
eqs_pre_inhi = '''
dX_a/dt = (-X_a + tm_inhi*(j_pyr_inhi*x1 + j_ext_inhi*x2))/tra_inhi : weber (event-driven)
dX_g/dt = (-X_g + tm_inhi*j_int_inhi*x3)/trg : weber (event-driven)
X_a_tot_post = X_a : 1 (summed)
X_g_tot_post = X_g : 1 (summed)
x1 : 1
x2 : 1
x3 : 1
w : 1
'''

eqs_pre_exci = '''
dX_a/dt = (-X_a + tm_exci*(j_pyr_exci*x1 + j_ext_exci*x2))/tra_exci : weber (event-driven)
dX_g/dt = (-X_g + tm_exci*j_int_exci*x3)/trg : weber (event-driven)
X_a_tot_post = X_a : 1 (summed)
X_g_tot_post = X_g : 1 (summed)
x1 : 1
x2 : 1
x3 : 1
w : 1
'''


I = NeuronGroup(N_inhi, eqs_inhi, threshold='v>v_thre', reset='v=v_rese',
                    refractory=tr_inhi, method='exact')
I.v = v_rest

E = NeuronGroup(N_exci, eqs_exci, threshold='v>v_thre', reset='v=v_rese',
                    refractory=tr_exci, method='exact')
E.v = v_rest

EE = Synapses(E, E, model = eqs_pre_exci, delay=tl, on_pre='x1 += w')


M_inhi = SpikeMonitor(I)
M_exci = SpikeMonitor(E)
run(duration)
