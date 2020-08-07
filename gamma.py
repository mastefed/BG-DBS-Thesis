from brian2 import *
import matplotlib.pyplot as plt

N = 5000
N_inhi = 1000
N_exci = 4000
duration = 10*ms

dim_corr = 1*mV/(volt*second)

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

# Modello le equazioni per le reti di neuroni inibitori ed eccitatori
eqs_inhi = '''
dv/dt = (-v + I_a - I_g)/tm_inhi : volt (unless refractory)
dI_a/dt = (-I_a + X_a_tot + X_ext_tot)/tda_inhi : volt
dI_g/dt = (-I_g + X_g_tot)/tdg : volt
X_a_tot : volt
X_g_tot : volt
X_ext_tot : volt
'''

# La differenza me la ritrovo nelle costanti temporali
eqs_exci = '''
dv/dt = (-v + I_a - I_g)/tm_exci : volt (unless refractory)
dI_a/dt = (-I_a + X_a_tot + X_ext_tot)/tda_exci : volt
dI_g/dt = (-I_g + X_g_tot)/tdg : volt
X_a_tot : volt
X_g_tot : volt
X_ext_tot : volt
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

eqs_ext_to_inhi = '''
dX_ext/dt = -X_ext/tra_inhi : volt (event-driven)
X_ext_tot_post = X_ext : volt (summed)
'''

eqs_ext_to_exci = '''
dX_ext/dt = -X_ext/tra_exci : volt (event-driven)
X_ext_tot_post = X_ext : volt (summed)
'''

# Modello le reti di neuroni che mi servono
I = NeuronGroup(N_inhi, eqs_inhi, threshold='v>v_thre', reset='v=v_rese',
                    refractory=tr_inhi, method='exact')
I.v = v_rest

E = NeuronGroup(N_exci, eqs_exci, threshold='v>v_thre', reset='v=v_rese',
                    refractory=tr_exci, method='exact')
E.v = v_rest

EE = Synapses(E, E, model=eqs_exci_to_exci, delay=tl, on_pre='X_a += tm_exci*j_exci_exci*dim_corr')
II = Synapses(I, I, model=eqs_inhi_to_inhi, delay=tl, on_pre='X_g += tm_inhi*j_inhi_inhi*dim_corr')
EI = Synapses(E, I, model=eqs_exci_to_inhi, delay=tl, on_pre='X_a += tm_exci*j_exci_inhi*dim_corr')
IE = Synapses(I, E, model=eqs_inhi_to_exci, delay=tl, on_pre='X_g += tm_inhi*j_inhi_inhi*dim_corr')

EE.connect(p=p)
EI.connect(p=p)
IE.connect(p=p)
II.connect(p=p)

# Provo a modellare il noise seguendo la guida di Brian2 sui PoissonGroup

sigma_n = 0.4*Hz
tau_n = 16*ms
ni_0 = 2*Hz

rates = '''
ni = ni_0 + n : Hz
dn/dt = (-n + sigma_n*xi*sqrt(2/tau_n))/tau_n : Hz
'''

Ext = NeuronGroup(N_exci, rates, threshold='rand()<ni*dt')
ExtE = Synapses(Ext, E, model=eqs_ext_to_exci, delay=tl, on_pre='X_ext += tm_exci*j_ext_exci*dim_corr')
ExtI = Synapses(Ext, I, model=eqs_ext_to_inhi, delay=tl, on_pre='X_ext += tm_exci*j_ext_inhi*dim_corr')
ExtE.connect()
ExtI.connect()

M_inhi = SpikeMonitor(I)
M_exci = SpikeMonitor(E)
run(duration)
