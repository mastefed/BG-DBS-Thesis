import brian2 as b2
import random
import numpy as np
from matplotlib import pyplot as plt

from parameters import *
from equations import *

def connmatrix(num_postsyn, num_presyn, num_conn):
    s = (num_presyn, num_postsyn)
    connections = np.zeros(s)
    for k, j in enumerate(random.sample(range(num_postsyn), num_postsyn)):
        for h, i in enumerate(random.sample(range(num_presyn), num_conn)):
            connections[i,j] = 1
    sources, targets = connections.nonzero()
    return targets, sources

def create_synapses(N_pre, N_post, indegree, autapse=True):
    """ Create random connections between two groups or within one group.
        :param N_pre: number of neurons in pre group
        :param N_post: number of neurons in post group
        :param c:   connectivity
        :param autapse: whether to allow autapses (connection of neuron to itself if pre = post population)
        :return: 2xN_con array of connection indices (pre-post pairs)
    """

    i = np.array([], dtype=int)
    j = np.array([], dtype=int)

    for n in range(N_post):

        if not autapse: # if autapses are disabled, remove index of present post neuron from pre options
            opts = np.delete(np.arange(N_pre, dtype=int), n)
        else:
            opts = np.arange(N_pre, dtype=int)

        pre = np.random.choice(opts, indegree, replace=False)

        # add connection indices to list
        i = np.hstack((i, pre))
        j = np.hstack((j, np.repeat(n, indegree)))

    return np.array([i, j])

fsnpars = neuronparameters['FSN']
d1pars = neuronparameters['D1']
d2pars = neuronparameters['D2']
stnpars = neuronparameters['STN']
gptipars = neuronparameters['GPTI']
gptapars = neuronparameters['GPTA']
gpipars = neuronparameters['GPI']

##### Neuron Populations ---------->
##### D1 Population
t_ref_d1 = d1pars['t_ref']*b2.ms
V_th_d1 = d1pars['V_th']*b2.mV
V_reset_d1 = d1pars['V_reset']*b2.mV

D1 = b2.NeuronGroup(neuron['D1'], leakyif, method='exponential_euler', threshold='V>V_th_d1', reset='V=V_reset_d1',
refractory=t_ref_d1)

D1.C_m = d1pars['C_m']*b2.pfarad
D1.g_L = d1pars['g_L']*b2.nsiemens
D1.I_e = d1pars['I_e']*b2.pamp
D1.E_L = d1pars['E_L']*b2.mV
D1.E_ex = d1pars['E_ex']*b2.mV
D1.E_in = d1pars['E_in']*b2.mV
D1.tau_syn_ex = d1pars['tau_syn_ex']*b2.ms
D1.tau_syn_in = d1pars['tau_syn_in']*b2.ms

D1.V = d1pars['V_m']*b2.mV

##### D2 Population
t_ref_d2 = d2pars['t_ref']*b2.ms
V_th_d2 = d2pars['V_th']*b2.mV
V_reset_d2 = d2pars['V_reset']*b2.mV

D2 = b2.NeuronGroup(neuron['D2'], leakyif, method='exponential_euler', threshold='V>V_th_d2', reset='V=V_reset_d2',
refractory=t_ref_d2)

D2.C_m = d2pars['C_m']*b2.pfarad
D2.g_L = d2pars['g_L']*b2.nsiemens
D2.I_e = d2pars['I_e']*b2.pamp
D2.E_L = d2pars['E_L']*b2.mV
D2.E_ex = d2pars['E_ex']*b2.mV
D2.E_in = d2pars['E_in']*b2.mV
D2.tau_syn_ex = d2pars['tau_syn_ex']*b2.ms
D2.tau_syn_in = d2pars['tau_syn_in']*b2.ms

D2.V = d2pars['V_m']*b2.mV

##### FSN Population
t_ref_fsn = fsnpars['t_ref']*b2.ms
V_th_fsn = fsnpars['V_th']*b2.mV
V_reset_fsn = fsnpars['V_reset']*b2.mV

FSN = b2.NeuronGroup(neuron['FSN'], leakyif, method='exponential_euler', threshold='V>V_th_fsn', reset='V=V_reset_fsn',
refractory=t_ref_fsn)

FSN.C_m = fsnpars['C_m']*b2.pfarad
FSN.g_L = fsnpars['g_L']*b2.nsiemens
FSN.I_e = fsnpars['I_e']*b2.pamp
FSN.E_L = fsnpars['E_L']*b2.mV
FSN.E_ex = fsnpars['E_ex']*b2.mV
FSN.E_in = fsnpars['E_in']*b2.mV
FSN.tau_syn_ex = fsnpars['tau_syn_ex']*b2.ms
FSN.tau_syn_in = fsnpars['tau_syn_in']*b2.ms

FSN.V = fsnpars['V_m']*b2.mV

##### STN Population
V_peak_stn = stnpars['V_peak']*b2.mV
V_reset_stn = stnpars['V_reset']*b2.mV
b_stn = stnpars['b']*b2.pamp

STN = b2.NeuronGroup(neuron['STN'], adexif, method='exponential_euler', threshold='V>V_peak_stn', reset='V=V_reset_stn;w=w+b_stn')

STN.C_m = stnpars['C_m']*b2.pfarad
STN.g_L = stnpars['g_L']*b2.nsiemens
STN.E_L = stnpars['E_L']*b2.mV
STN.I_e = stnpars['I_e']*b2.pamp
STN.Delta_T = stnpars['Delta_T']*b2.mV
STN.E_ex = stnpars['E_ex']*b2.mV
STN.E_in = stnpars['E_in']*b2.mV
STN.a = stnpars['a']*b2.nsiemens
STN.tau_w = stnpars['tau_w']*b2.ms
STN.V_th = stnpars['V_th']*b2.mV
STN.tau_syn_ex = stnpars['tau_syn_ex']*b2.ms
STN.tau_syn_in = stnpars['tau_syn_in']*b2.ms

STN.V = stnpars['V_m']*b2.mV

##### GPe Prototypical Population (projecting to STN)
V_peak_gpti = gptipars['V_peak']*b2.mV
V_reset_gpti = gptipars['V_reset']*b2.mV
b_gpti = gptipars['b']*b2.pamp

GPTI = b2.NeuronGroup(neuron['GPTI'], adexif, method='exponential_euler', threshold='V>V_peak_gpti', reset='V=V_reset_gpti;w=w+b_gpti')

GPTI.C_m = gptipars['C_m']*b2.pfarad
GPTI.g_L = gptipars['g_L']*b2.nsiemens
GPTI.E_L = gptipars['E_L']*b2.mV
GPTI.I_e = gptipars['I_e']*b2.pamp
GPTI.Delta_T = gptipars['Delta_T']*b2.mV
GPTI.E_ex = gptipars['E_ex']*b2.mV
GPTI.E_in = gptipars['E_in']*b2.mV
GPTI.a = gptipars['a']*b2.nsiemens
GPTI.tau_w = gptipars['tau_w']*b2.ms
GPTI.V_th = gptipars['V_th']*b2.mV
GPTI.tau_syn_ex = gptipars['tau_syn_ex']*b2.ms
GPTI.tau_syn_in = gptipars['tau_syn_in']*b2.ms

GPTI.V = gptipars['V_m']*b2.mV

##### GPe Arkypallidal Population (projecting to MSN)
V_peak_gpta = gptapars['V_peak']*b2.mV
V_reset_gpta = gptapars['V_reset']*b2.mV
b_gpta = gptapars['b']*b2.pamp

GPTA = b2.NeuronGroup(neuron['GPTA'], adexif, method='exponential_euler', threshold='V>V_peak_gpta', reset='V=V_reset_gpta;w=w+b_gpta')

GPTA.C_m = gptapars['C_m']*b2.pfarad
GPTA.g_L = gptapars['g_L']*b2.nsiemens
GPTA.E_L = gptapars['E_L']*b2.mV
GPTA.I_e = gptapars['I_e']*b2.pamp
GPTA.Delta_T = gptapars['Delta_T']*b2.mV
GPTA.E_ex = gptapars['E_ex']*b2.mV
GPTA.E_in = gptapars['E_in']*b2.mV
GPTA.a = gptapars['a']*b2.nsiemens
GPTA.tau_w = gptapars['tau_w']*b2.ms
GPTA.V_th = gptapars['V_th']*b2.mV
GPTA.tau_syn_ex = gptapars['tau_syn_ex']*b2.ms
GPTA.tau_syn_in = gptapars['tau_syn_in']*b2.ms

GPTA.V = gptapars['V_m']*b2.mV

##### GPi
V_peak_gpi = gpipars['V_peak']*b2.mV
V_reset_gpi = gpipars['V_reset']*b2.mV
b_gpi = gpipars['b']*b2.pamp

GPI = b2.NeuronGroup(neuron['GPI'], adexif, method='exponential_euler', threshold='V>V_peak_gpi', reset='V=V_reset_gpi;w=w+b_gpi')

GPI.C_m = gpipars['C_m']*b2.pfarad
GPI.g_L = gpipars['g_L']*b2.nsiemens
GPI.E_L = gpipars['E_L']*b2.mV
GPI.I_e = gpipars['I_e']*b2.pamp
GPI.Delta_T = gpipars['Delta_T']*b2.mV
GPI.E_ex = gpipars['E_ex']*b2.mV
GPI.E_in = gpipars['E_in']*b2.mV
GPI.a = gpipars['a']*b2.nsiemens
GPI.tau_w = gpipars['tau_w']*b2.ms
GPI.V_th = gpipars['V_th']*b2.mV
GPI.tau_syn_ex = gpipars['tau_syn_ex']*b2.ms
GPI.tau_syn_in = gpipars['tau_syn_in']*b2.ms

GPI.V = gpipars['V_m']*b2.mV

##### Poisson Noise
noisefsnpars = poissoninput['FSN']
noised1pars = poissoninput['D1']
noised2pars = poissoninput['D2']
noisestnpars = poissoninput['STN']
noisegptipars = poissoninput['GPTI']
noisegptapars = poissoninput['GPTA']
noisegpipars = poissoninput['GPI']

c = 0.

ratenoisefsn = noisefsnpars['rate']*b2.Hz
noisefsn = b2.NeuronGroup(noisefsnpars['num'], 'v : 1 (shared)', threshold='((v < ratenoisefsn*dt) and rand() < sqrt(c)) or rand() < ratenoisefsn*(1 - sqrt(c))*dt')
noisefsn.run_regularly('v = rand()')

ratenoised1 = noised1pars['rate']*b2.Hz
noised1 = b2.NeuronGroup(noised1pars['num'], 'v : 1 (shared)', threshold='((v < ratenoised1*dt) and rand() < sqrt(c)) or rand() < ratenoised1*(1 - sqrt(c))*dt')
noised1.run_regularly('v = rand()')

ratenoised2 = noised2pars['rate']*b2.Hz
noised2 = b2.NeuronGroup(noised2pars['num'], 'v : 1 (shared)', threshold='((v < ratenoised2*dt) and rand() < sqrt(c)) or rand() < ratenoised2*(1 - sqrt(c))*dt')
noised2.run_regularly('v = rand()')

noisestn = b2.PoissonGroup(noisestnpars['num'], rates=noisestnpars['rate']*b2.Hz)
noisegpti = b2.PoissonGroup(noisegptipars['num'], rates=noisegptipars['rate']*b2.Hz)
noisegpta = b2.PoissonGroup(noisegptapars['num'], rates=noisegptapars['rate']*b2.Hz)
noisegpi = b2.PoissonGroup(noisegpipars['num'], rates=noisegpipars['rate']*b2.Hz)

mulval = 0.1*b2.nsiemens

weightnoisefsn = noisefsnpars['weight']*b2.nsiemens
noisetofsn = b2.Synapses(noisefsn, FSN, delay=noisefsnpars['delay']*b2.ms, on_pre='g_e += weightnoisefsn + mulval*rand()')
noisetofsn.connect(j='i')

weightnoised1 = noised1pars['weight']*b2.nsiemens
noisetod1 = b2.Synapses(noised1, D1, delay=noised1pars['delay']*b2.ms, on_pre='g_e += weightnoised1 + mulval*rand()')
noisetod1.connect(j='i')

weightnoised2 = noised2pars['weight']*b2.nsiemens
noisetod2 = b2.Synapses(noised2, D2, delay=noised2pars['delay']*b2.ms, on_pre='g_e += weightnoised2 + mulval*rand()')
noisetod2.connect(j='i')

weightnoisestn = noisestnpars['weight']*b2.nsiemens
noisetostn = b2.Synapses(noisestn, STN, delay=noisestnpars['delay']*b2.ms, on_pre='g_e += weightnoisestn + mulval*rand()')
noisetostn.connect(j='i')

weightnoisegpti = noisegptipars['weight']*b2.nsiemens
noisetogpti = b2.Synapses(noisegpti, GPTI, delay=noisegptipars['delay']*b2.ms, on_pre='g_e += weightnoisegpti + mulval*rand()')
noisetogpti.connect(j='i')

weightnoisegpta = noisegptapars['weight']*b2.nsiemens
noisetogpta = b2.Synapses(noisegpta, GPTA, delay=noisegptapars['delay']*b2.ms, on_pre='g_e += weightnoisegpta + mulval*rand()')
noisetogpta.connect(j='i')

weightnoisegpi = noisegpipars['weight']*b2.nsiemens
noisetogpi = b2.Synapses(noisegpi, GPI, delay=noisegpipars['delay']*b2.ms, on_pre='g_e += weightnoisegpi + mulval*rand()')
noisetogpi.connect(j='i')


##### Synapses
# Synapses to D1
synd1pars = staticsyn['D1']

# connection lists for D1
connections = {}
pre_idx, post_idx = create_synapses(neuron['D1'], neuron['D1'], synd1pars['D1']['degree'], autapse=False)
connections['d1d1'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['D2'], neuron['D1'], synd1pars['D2']['degree'])
connections['d2d1'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['FSN'], neuron['D1'], synd1pars['FSN']['degree'])
connections['fsnd1'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['GPTA'], neuron['D1'], synd1pars['GPTA']['degree'])
connections['gptad1'] = np.array([pre_idx, post_idx])

# D1 --> D1
weightd1d1 = synd1pars['D1']['weight']*b2.nsiemens
d1tod1 = b2.Synapses(D1, D1, delay=synd1pars['D1']['delay']*b2.ms, on_pre='g_i += weightd1d1')
d1tod1.connect(i=connections['d1d1'][0], j=connections['d1d1'][1])

# D2 --> D1
weightd2d1 = synd1pars['D2']['weight']*b2.nsiemens
d2tod1 = b2.Synapses(D2, D1, delay=synd1pars['D2']['delay']*b2.ms, on_pre='g_i += weightd2d1')
d2tod1.connect(i=connections['d2d1'][0], j=connections['d2d1'][1])

# FSN --> D1
weightfsnd1 = synd1pars['FSN']['weight']*b2.nsiemens
fsntod1 = b2.Synapses(FSN, D1, delay=synd1pars['FSN']['delay']*b2.ms, on_pre='g_i += weightfsnd1')
fsntod1.connect(i=connections['fsnd1'][0], j=connections['fsnd1'][1])

# GPTA --> D1
weightgptad1 = synd1pars['GPTA']['weight']*b2.nsiemens
gptatod1 = b2.Synapses(GPTA, D1, delay=synd1pars['GPTA']['delay']*b2.ms, on_pre='g_i += weightgptad1')
gptatod1.connect(i=connections['gptad1'][0], j=connections['gptad1'][1])

# Synapses to D2
synd2pars = staticsyn['D2']

# connection lists for D2
pre_idx, post_idx = create_synapses(neuron['D2'], neuron['D2'], synd2pars['D2']['degree'], autapse=False)
connections['d2d2'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['D1'], neuron['D2'], synd2pars['D1']['degree'])
connections['d1d2'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['FSN'], neuron['D2'], synd2pars['FSN']['degree'])
connections['fsnd2'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['GPTA'], neuron['D2'], synd2pars['GPTA']['degree'])
connections['gptad2'] = np.array([pre_idx, post_idx])

# D1 --> D2
weightd1d2 = synd2pars['D1']['weight']*b2.nsiemens
d1tod2 = b2.Synapses(D1, D2, delay=synd2pars['D1']['delay']*b2.ms, on_pre='g_i += weightd1d1')
d1tod2.connect(i=connections['d1d2'][0], j=connections['d1d2'][1])

# D2 --> D2
weightd2d2 = synd2pars['D2']['weight']*b2.nsiemens
d2tod2 = b2.Synapses(D2, D2, delay=synd2pars['D2']['delay']*b2.ms, on_pre='g_i += weightd2d1')
d2tod2.connect(i=connections['d2d2'][0], j=connections['d2d2'][1])

# FSN --> D2
weightfsnd2 = synd2pars['FSN']['weight']*b2.nsiemens
fsntod2 = b2.Synapses(FSN, D2, delay=synd2pars['FSN']['delay']*b2.ms, on_pre='g_i += weightfsnd1')
fsntod2.connect(i=connections['fsnd2'][0], j=connections['fsnd2'][1])

# GPTA --> D2
weightgptad2 = synd2pars['GPTA']['weight']*b2.nsiemens
gptatod2 = b2.Synapses(GPTA, D2, delay=synd2pars['GPTA']['delay']*b2.ms, on_pre='g_i += weightgptad1')
gptatod2.connect(i=connections['gptad2'][0], j=connections['gptad2'][1])


# Synapses to FSN
synfsnpars = staticsyn['FSN']

# connection lists for FSN
pre_idx, post_idx = create_synapses(neuron['FSN'], neuron['FSN'], synfsnpars['FSN']['degree'], autapse=False)
connections['fsnfsn'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['D2'], neuron['FSN'], synfsnpars['D2']['degree'])
connections['d2fsn'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['D1'], neuron['FSN'], synfsnpars['D1']['degree'])
connections['d1fsn'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['GPTA'], neuron['FSN'], synfsnpars['GPTA']['degree'])
connections['gptafsn'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['GPTI'], neuron['FSN'], synfsnpars['GPTI']['degree'])
connections['gptifsn'] = np.array([pre_idx, post_idx])

# D1 --> FSN
weightd1fsn = synfsnpars['D1']['weight']*b2.nsiemens
d1tofsn = b2.Synapses(D1, FSN, delay=synfsnpars['D1']['delay']*b2.ms, on_pre='g_i += weightd1fsn')
d1tofsn.connect(i=connections['d1fsn'][0], j=connections['d1fsn'][1])

# D2 --> FSN
weightd2fsn = synfsnpars['D2']['weight']*b2.nsiemens
d2tofsn = b2.Synapses(D2, FSN, delay=synfsnpars['D2']['delay']*b2.ms, on_pre='g_i += weightd2fsn')
d2tofsn.connect(i=connections['d2fsn'][0], j=connections['d2fsn'][1])

# FSN --> FSN
weightfsnfsn = synfsnpars['FSN']['weight']*b2.nsiemens
fsntofsn = b2.Synapses(FSN, FSN, delay=synfsnpars['FSN']['delay']*b2.ms, on_pre='g_i += weightfsnfsn')
fsntofsn.connect(i=connections['fsnfsn'][0], j=connections['fsnfsn'][1])

# GPTA --> FSN
weightgptafsn = synfsnpars['GPTA']['weight']*b2.nsiemens
gptatofsn = b2.Synapses(GPTA, FSN, delay=synfsnpars['GPTA']['delay']*b2.ms, on_pre='g_i += weightgptafsn')
gptatofsn.connect(i=connections['gptafsn'][0], j=connections['gptafsn'][1])

# GPTI --> FSN
weightgptifsn = synfsnpars['GPTI']['weight']*b2.nsiemens
gptitofsn = b2.Synapses(GPTI, FSN, delay=synfsnpars['GPTI']['delay']*b2.ms, on_pre='g_i += weightgptifsn')
gptitofsn.connect(i=connections['gptifsn'][0], j=connections['gptifsn'][1])

# Synapses to GPTA 
syngptapars = staticsyn['GPTA']

# connection lists for GPTA
pre_idx, post_idx = create_synapses(neuron['GPTA'], neuron['GPTA'], syngptapars['GPTA']['degree'], autapse=False)
connections['gptagpta'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['FSN'], neuron['GPTA'], syngptapars['FSN']['degree'])
connections['fsngpta'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['GPTI'], neuron['GPTA'], syngptapars['GPTI']['degree'])
connections['gptigpta'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['STN'], neuron['GPTA'], syngptapars['STN']['degree'])
connections['stngpta'] = np.array([pre_idx, post_idx])

# FSN --> GPTA
weightfsngpta = syngptapars['FSN']['weight']*b2.nsiemens
fsntogpta = b2.Synapses(FSN, GPTA, delay=syngptapars['FSN']['delay']*b2.ms, on_pre='g_i += weightfsngpta')
fsntogpta.connect(i=connections['fsngpta'][0], j=connections['fsngpta'][1])

# GPTA --> GPTA
weightgptagpta = syngptapars['GPTA']['weight']*b2.nsiemens
gptatogpta = b2.Synapses(GPTA, GPTA, delay=syngptapars['GPTA']['delay']*b2.ms, on_pre='g_i += weightgptagpta')
gptatogpta.connect(i=connections['gptagpta'][0], j=connections['gptagpta'][1])

# GPTI --> GPTA
weightgptigpta = syngptapars['GPTI']['weight']*b2.nsiemens
gptitogpta = b2.Synapses(GPTI, GPTA, delay=syngptapars['GPTI']['delay']*b2.ms, on_pre='g_i += weightgptigpta')
gptitogpta.connect(i=connections['gptigpta'][0], j=connections['gptigpta'][1])

# STN --> GPTA
weightstngpta = syngptapars['STN']['weight']*b2.nsiemens
stntogpta = b2.Synapses(STN, GPTA, delay=syngptapars['STN']['delay']*b2.ms, on_pre='g_e += weightstngpta')
stntogpta.connect(i=connections['stngpta'][0], j=connections['stngpta'][1])


# Synapses to GPTI 
syngptipars = staticsyn['GPTI']

# connection lists for GPTI
pre_idx, post_idx = create_synapses(neuron['GPTI'], neuron['GPTI'], syngptipars['GPTI']['degree'], autapse=False)
connections['gptigpti'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['FSN'], neuron['GPTI'], syngptipars['FSN']['degree'])
connections['fsngpti'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['GPTA'], neuron['GPTI'], syngptipars['GPTA']['degree'])
connections['gptagpti'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['D2'], neuron['GPTI'], syngptipars['D2']['degree'])
connections['d2gpti'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['STN'], neuron['GPTI'], syngptipars['STN']['degree'])
connections['stngpti'] = np.array([pre_idx, post_idx])

# D2 --> GPTI
weightd2gpti = syngptipars['D2']['weight']*b2.nsiemens
d2togpti = b2.Synapses(D2, GPTI, delay=syngptipars['D2']['delay']*b2.ms, on_pre='g_i += weightd2gpti')
d2togpti.connect(i=connections['d2gpti'][0], j=connections['d2gpti'][1])

# FSN --> GPTI
weightfsngpti = syngptipars['FSN']['weight']*b2.nsiemens
fsntogpti = b2.Synapses(FSN, GPTI, delay=syngptipars['FSN']['delay']*b2.ms, on_pre='g_i += weightfsngpti')
fsntogpti.connect(i=connections['fsngpti'][0], j=connections['fsngpti'][1])

# GPTA --> GPTI
weightgptagpti = syngptipars['GPTA']['weight']*b2.nsiemens
gptatogpti = b2.Synapses(GPTA, GPTI, delay=syngptipars['GPTA']['delay']*b2.ms, on_pre='g_i += weightgptagpti')
gptatogpti.connect(i=connections['gptagpti'][0], j=connections['gptagpti'][1])

# GPTI --> GPTI
weightgptigpti = syngptipars['GPTI']['weight']*b2.nsiemens
gptitogpti = b2.Synapses(GPTI, GPTI, delay=syngptipars['GPTI']['delay']*b2.ms, on_pre='g_i += weightgptigpti')
gptitogpti.connect(i=connections['gptigpti'][0], j=connections['gptigpti'][1])

# STN --> GPTI
weightstngpti = syngptipars['STN']['weight']*b2.nsiemens
stntogpti = b2.Synapses(STN, GPTI, delay=syngptipars['STN']['delay']*b2.ms, on_pre='g_e += weightstngpti')
stntogpti.connect(i=connections['stngpti'][0], j=connections['stngpti'][1])


# Synapses to STN
synstnpars = staticsyn['STN']

# connection lists for STN
pre_idx, post_idx = create_synapses(neuron['GPTI'], neuron['STN'], synstnpars['GPTI']['degree'])
connections['gptistn'] = np.array([pre_idx, post_idx])

# GPTI --> STN
weightgptistn = synstnpars['GPTI']['weight']*b2.nsiemens
gptitostn = b2.Synapses(GPTI, STN, delay=synstnpars['GPTI']['delay']*b2.ms, on_pre='g_i += weightgptistn')
gptitostn.connect(i=connections['gptistn'][0], j=connections['gptistn'][1])


# Synapses to GPi
syngpipars = staticsyn['GPI']

# connection lists for GPI
pre_idx, post_idx = create_synapses(neuron['D1'], neuron['GPI'], syngpipars['D1']['degree'], autapse=False)
connections['d1gpi'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['GPTI'], neuron['GPI'], syngpipars['GPTI']['degree'])
connections['gptigpi'] = np.array([pre_idx, post_idx])
pre_idx, post_idx = create_synapses(neuron['STN'], neuron['GPI'], syngpipars['STN']['degree'])
connections['stngpi'] = np.array([pre_idx, post_idx])

# D1 --> GPi
weightd1gpi = syngpipars['D1']['weight']*b2.nsiemens
d1togpi = b2.Synapses(D1, GPI, delay=syngpipars['D1']['delay']*b2.ms, on_pre='g_i += weightd1gpi')
d1togpi.connect(i=connections['d1gpi'][0], j=connections['d1gpi'][1])

# GPTI --> GPi
weightgptigpi = syngpipars['GPTI']['weight']*b2.nsiemens
gptitogpi = b2.Synapses(GPTI, GPI, delay=syngpipars['GPTI']['delay']*b2.ms, on_pre='g_i += weightgptigpi')
gptitogpi.connect(i=connections['gptigpi'][0], j=connections['gptigpi'][1])

# STN --> GPi
weightstngpi = syngpipars['STN']['weight']*b2.nsiemens
stntogpi = b2.Synapses(STN, GPI, delay=syngpipars['STN']['delay']*b2.ms, on_pre='g_e += weightstngpi')
stntogpi.connect(i=connections['stngpi'][0], j=connections['stngpi'][1])

"""
inp = b2.SpikeGeneratorGroup(1, np.array([0,0,0]), np.array([400,600,800])*b2.ms)

feedforwardd1 = b2.Synapses(inp, D1, on_pre='g_e += 1*nS; g_i += -1*nS')
feedforwardd1.connect()

feedforwardd2 = b2.Synapses(inp, D2, on_pre='g_e += 1*nS; g_i += -1*nS')
feedforwardd2.connect()

feedforwardfsn = b2.Synapses(inp, FSN, on_pre='g_e += 1*nS; g_i += -1*nS')
feedforwardfsn.connect()

feedforwardgpta = b2.Synapses(inp, GPTA, on_pre='g_e += 1*nS; g_i += -1*nS')
feedforwardgpta.connect()

feedforwardgpti = b2.Synapses(inp, GPTI, on_pre='g_e += 1*nS; g_i += -1*nS')
feedforwardgpti.connect()

feedforwardstn = b2.Synapses(inp, STN, on_pre='g_e += 1*nS; g_i += -1*nS')
feedforwardstn.connect()

feedforwardgpi = b2.Synapses(inp, GPI, on_pre='g_e += 1*nS; g_i += -1*nS')
feedforwardgpi.connect()
"""
