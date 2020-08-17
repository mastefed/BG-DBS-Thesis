from brian2 import *
import matplotlib.pyplot as plt
import numpy as np

N = 5000
N_inhi = 1000
N_exci = 4000
duration = 200*ms

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

# Synaptic efficacies inhi/exci/ext to inhi
j_inhi_inhi = 2.7*mV
j_exci_inhi = 0.7*mV
j_ext_inhi = 0.95*mV

# Synaptic efficacies inhi/exci/ext to exci
j_inhi_exci = 1.7*mV
j_exci_exci = 0.42*mV
j_ext_exci = 0.55*mV

sigma_n = 0.5*Hz
tau_n = 16*ms
v_signal = 2*Hz

# Modello le equazioni per le reti di neuroni inibitori ed eccitatori
eqs_inhi = '''
dv/dt = (-v + I_a - I_g)/tm_inhi : volt (unless refractory)
dI_a/dt = (-I_a + X_a_tot)/tda_inhi : volt
dI_g/dt = (-I_g + X_g_tot)/tdg : volt
X_a_tot : volt
X_g_tot : volt
'''

# La differenza me la ritrovo nelle costanti temporali
eqs_exci = '''
dv/dt = (-v + I_a - I_g)/tm_exci : volt (unless refractory)
dI_a/dt = (-I_a + X_a_tot)/tda_exci : volt
dI_g/dt = (-I_g + X_g_tot)/tdg : volt
X_a_tot : volt
X_g_tot : volt
'''

# Modello le equazioni per le correnti sinaptiche
eqs_exci_to_inhi = '''
dX_a/dt = -X_a/tra_inhi : volt (event-driven)
X_a_tot_post = X_a : volt (summed)
'''

eqs_inhi_to_exci = '''
dX_g/dt = -X_g/trg : volt (event-driven)
X_g_tot_post = X_g : volt (summed)
'''

eqs_exci_to_exci = '''
dX_a/dt = -X_a/tra_exci : volt (event-driven)
X_a_tot_post = X_a : volt (summed)
'''

eqs_inhi_to_inhi = '''
dX_g/dt = -X_g/trg : volt (event-driven)
X_g_tot_post = X_g : volt (summed)
'''

# Modello le reti di neuroni che mi servono
I = NeuronGroup(N_inhi, eqs_inhi, threshold='v>v_thre', reset='v=v_rese',
                    refractory=tr_inhi, method='euler')
I.v = v_rest

E = NeuronGroup(N_exci, eqs_exci, threshold='v>v_thre', reset='v=v_rese',
                    refractory=tr_exci, method='euler')
E.v = v_rest

EE = Synapses(E, E, model=eqs_exci_to_exci, delay=tl, on_pre='X_a += tm_exci*j_exci_exci/tra_exci')
II = Synapses(I, I, model=eqs_inhi_to_inhi, delay=tl, on_pre='X_g += tm_inhi*j_inhi_inhi/tra_inhi')
EI = Synapses(E, I, model=eqs_exci_to_inhi, delay=tl, on_pre='X_a += tm_exci*j_exci_inhi/tra_exci')
IE = Synapses(I, E, model=eqs_inhi_to_exci, delay=tl, on_pre='X_g += tm_inhi*j_inhi_inhi/tra_inhi')

EE.connect(p=p)
EI.connect(p=p)
IE.connect(p=p)
II.connect(p=p)

P1 = PoissonInput(E, 'X_a_tot', N_exci, 2*Hz, 'tm_exci*j_ext_exci/tra_exci')
P2 = PoissonInput(I, 'X_a_tot', N_inhi, 2*Hz, 'tm_exci*j_ext_inhi/tra_exci')

M_inhi = SpikeMonitor(I)
M_exci = SpikeMonitor(E)
S_inhi = StateMonitor(I, ['v', 'I_a', 'I_g'], record=True)
S_exci = StateMonitor(E, ['v', 'I_a', 'I_g'], record=True)
run(duration)


plt.figure("Raster plots")
plt.subplot(211)
plt.ylabel("Neuron (exc) Index")
plt.xlim((0, duration))
plt.plot(M_exci.t/ms, M_exci.i, '.', ms='2')
plt.subplot(212)
plt.ylabel("Neuron (inh) Index")
plt.xlabel("Time (ms)")
plt.xlim((0, duration))
plt.plot(M_inhi.t/ms, M_inhi.i, '.', ms='2')


plt.figure("Voltage Membrane of a Single Neuron")
plt.subplot(211)
plt.ylim((0,0.021))
plt.plot(S_exci.t, S_exci.v[0])
plt.ylabel("One exc neuron V (mV)")
plt.subplot(212)
plt.ylabel("One inh neuron V (mV)")
plt.xlabel("Time (ms)")
plt.ylim((0,0.021))
plt.plot(S_inhi.t, S_inhi.v[0])


plt.figure("Corrente I_a")
plt.plot(S_exci.I_a, 'r')
plt.plot(S_exci.I_g, 'b')
plt.plot(S_exci.I_a - S_exci.I_g, 'g')


plt.show()
