from brian2 import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

N_inhi = 1000
N_exci = 4000
duration = 500*ms

p = 0.2 # connectivity probability
freq = 3*Hz

v_rest = 0*mV  # resting potential
v_thre = 18*mV  # threshold potential
v_rese = 11*mV  # reset potential

tr_inhi = 1*ms  # refractory time for inhibitory group
tr_exci = 2*ms  # refractory time for excitatory group

tm_inhi = 10*ms  # time constant for inhibitory group
tm_exci = 20*ms  # time constant for excitatory group

tda_inhi = 1*ms  # decay time for ampa current into inhi neuron
tda_exci = 2*ms  # decay time for ampa current into exci neuron
tra_inhi = 0.2*ms  # rise time for ampa current into inhi neuron
tra_exci = 0.4*ms  # rise time for ampa current into exci neuron

tl = 1*ms  # latency of post-synaptic current

tdg = 5*ms  # decay time of gaba current
trg = 0.25*ms  # rise time of gaba current

# Synaptic efficacies inhi/exci/ext to inhi
j_inhi_inhi = 2.7*mV
j_exci_inhi = 0.7*mV
j_ext_inhi = 0.95*mV

# Synaptic efficacies inhi/exci/ext to exci
j_inhi_exci = 1.7*mV
j_exci_exci = 0.42*mV
j_ext_exci = 0.55*mV

# Modello le equazioni per le reti di neuroni inibitori ed eccitatori
eqs_inhi = '''
dv/dt = (-v + I_a - I_g)/tm_inhi : volt (unless refractory)
dI_a/dt = -I_a/tda_inhi + X_a/tda_inhi : volt
dX_a/dt = -X_a/tra_inhi : volt
dI_g/dt = (-I_g + X_g)/tdg : volt
dX_g/dt = -X_g/trg : volt
'''

# La differenza me la ritrovo nelle costanti temporali
eqs_exci = '''
dv/dt = (-v + I_a - I_g)/tm_exci : volt (unless refractory)
dI_a/dt = -I_a/tda_exci + X_a/tda_exci : volt
dX_a/dt = -X_a/tra_exci : volt
dI_g/dt = (-I_g + X_g)/tdg : volt
dX_g/dt = -X_g/trg : volt
'''



# Modello le reti di neuroni che mi servono
I = NeuronGroup(N_inhi, eqs_inhi, threshold='v>v_thre', reset='v=v_rese',
                    refractory=tr_inhi, method='euler')
I.v = v_rest

E = NeuronGroup(N_exci, eqs_exci, threshold='v>v_thre', reset='v=v_rese',
                    refractory=tr_exci, method='euler')
E.v = v_rest


EE = Synapses(E, E, delay=tl, on_pre='X_a += tm_exci*j_exci_exci/tra_exci') # /100k
II = Synapses(I, I, delay=tl, on_pre='X_g += tm_inhi*j_inhi_inhi/trg')
EI = Synapses(E, I, delay=tl, on_pre='X_a += tm_inhi*j_exci_inhi/tra_inhi')
IE = Synapses(I, E, delay=tl, on_pre='X_g += tm_exci*j_inhi_exci/trg') # *100k

P1 = PoissonInput(E, 'X_a', N_exci, freq, 'tm_exci*j_ext_exci/tra_exci')
P2 = PoissonInput(I, 'X_a', N_inhi, freq, 'tm_exci*j_ext_inhi/tra_inhi') # /100k

EE.connect(p=p)
EI.connect(p=p)
IE.connect(p=p)
II.connect(p=p)

M_inhi = SpikeMonitor(I)
M_exci = SpikeMonitor(E)
S_inhi = StateMonitor(I, ['v', 'I_a', 'I_g', 'X_a', 'X_g'], record=True)
S_exci = StateMonitor(E, ['v', 'I_a', 'I_g', 'X_a', 'X_g'], record=True)

run(duration)


plt.figure(1)
plt.title("Raster plot degli eccitatori")
plt.ylabel("Neuron (exc) Index")
plt.xlabel("Time (ms)")
plt.plot(M_exci.t/ms, M_exci.i, 'g.', ms='2')

plt.figure(2)
plt.title("Raster plot degli inibitori")
plt.ylabel("Neuron (inh) Index")
plt.xlabel("Time (ms)")
plt.plot(M_inhi.t/ms, M_inhi.i, 'r.', ms='2')


'''
plt.figure("Voltage Membrane of a Single Neuron")
plt.title("Test potenziale di membrane singolo neurone")
plt.subplot(211)
plt.ylim((0,0.021))
plt.plot(S_exci.t/ms, S_exci.v[0])
plt.ylabel("One exc neuron V (mV)")
plt.subplot(212)
plt.ylabel("One inh neuron V (mV)")
plt.xlabel("Time (ms)")
plt.ylim((0,0.021))
plt.plot(S_inhi.t/ms, S_inhi.v[0])
'''

'''
plt.figure(1)
plt.subplot(321)
plt.plot(S_exci.I_a.T, 'b')
plt.plot(S_exci.X_a.T, 'g')
plt.subplot(325)
plt.plot(S_exci.v.T/mV)
plt.subplot(322)
plt.plot(S_inhi.I_a.T, 'b')
plt.plot(S_inhi.X_a.T, 'g')
plt.subplot(326)
plt.plot(S_inhi.v.T/mV)
plt.subplot(323)
plt.plot(S_exci.I_g.T, 'b')
plt.plot(S_exci.X_g.T, 'g')
plt.subplot(324)
plt.plot(S_inhi.I_g.T, 'b')
plt.plot(S_inhi.X_g.T, 'g')
'''

mean_I_a_exci = np.mean(S_exci.I_a, 0)
mean_I_g_exci = np.mean(S_exci.I_g, 0)
mean_I_a_inhi = np.mean(S_inhi.I_a, 0)
mean_I_g_inhi = np.mean(S_inhi.I_g, 0)

mean_tot_curr_exci = abs(mean_I_a_exci) + abs(mean_I_g_exci)
mean_tot_curr_inhi = abs(mean_I_a_inhi) + abs(mean_I_g_inhi)

(f1, power_spectrum1) = signal.welch(mean_tot_curr_exci, fs=10000)
(f2, power_spectrum2) = signal.welch(mean_tot_curr_inhi, fs=10000)

plt.figure(3)
plt.subplot(211)
plt.plot(mean_tot_curr_exci, 'g')
plt.plot(mean_tot_curr_inhi, 'r')
plt.ylim((-0.2, 10))
plt.ylabel("Corrente (mV)")
plt.xlabel("Timesteps")
plt.subplot(212)
plt.xlim((0, 150))
plt.xlabel("f")
plt.plot(f1, power_spectrum1, 'g')
plt.plot(f2, power_spectrum2, 'r')




plt.show()
