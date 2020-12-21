from parameters import *
from equations import *

import brian2 as b2

#b2.clear_cache('cython')

fsnpars = neuronparameters['FSN']
d1pars = neuronparameters['D1']
d2pars = neuronparameters['D2']
stnpars = neuronparameters['STN']
gptipars = neuronparameters['GPTI']
gptapars = neuronparameters['GPTA']
gpipars = neuronparameters['GPI']

ctxfsnpars = poissoninput['FSN']
ctxd1pars = poissoninput['D1']
ctxd2pars = poissoninput['D2']
ctxstnpars = poissoninput['STN']
ctxgptipars = poissoninput['GPTI']
ctxgptapars = poissoninput['GPTA']
ctxgpipars = poissoninput['GPI']

##### Poisson Inputs
ctxforfsn = b2.PoissonGroup(1, rates=ctxfsnpars['rate']*b2.Hz)
ctxford1 = b2.PoissonGroup(1, rates=ctxd1pars['rate']*b2.Hz)
ctxford2 = b2.PoissonGroup(1, rates=ctxd2pars['rate']*b2.Hz)
ctxforstn = b2.PoissonGroup(1, rates=ctxstnpars['rate']*b2.Hz)
ctxforgpti = b2.PoissonGroup(1, rates=ctxgptipars['rate']*b2.Hz)
ctxforgpta = b2.PoissonGroup(1, rates=ctxgptapars['rate']*b2.Hz)
ctxforgpi = b2.PoissonGroup(1, rates=ctxgpipars['rate']*b2.Hz)

##### Neuron Populations ---------->
##### D1 Population
t_ref_d1 = d1pars['t_ref']*b2.ms
V_th_d1 = d1pars['V_th']*b2.mV
V_reset_d1 = d1pars['V_reset']*b2.mV

D1 = b2.NeuronGroup(neuron['D1'], leakyif, method='exact', threshold='V>V_th_d1', reset='V=V_reset_d1',
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

D2 = b2.NeuronGroup(neuron['D2'], leakyif, method='exact', threshold='V>V_th_d2', reset='V=V_reset_d2',
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

FSN = b2.NeuronGroup(neuron['FSN'], leakyif, method='exact', threshold='V>V_th_fsn', reset='V=V_reset_fsn',
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

STN = b2.NeuronGroup(neuron['STN'], adexif, method='euler', threshold='V>V_peak_stn', reset='V=V_reset_stn;w=w+b_stn')

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

GPTI = b2.NeuronGroup(neuron['GPTI'], adexif, method='euler', threshold='V>V_peak_gpti', reset='V=V_reset_gpti;w=w+b_gpti')

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

GPTA = b2.NeuronGroup(neuron['GPTA'], adexif, method='euler', threshold='V>V_peak_gpta', reset='V=V_reset_gpta;w=w+b_gpta')

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

GPI = b2.NeuronGroup(neuron['GPI'], adexif, method='euler', threshold='V>V_peak_gpi', reset='V=V_reset_gpi;w=w+b_gpi')

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
weightctxfsn = ctxfsnpars['weight']*b2.nsiemens
cortextofsn = b2.Synapses(ctxforfsn, FSN, delay=ctxfsnpars['delay']*b2.ms, on_pre='g_e += weightctxfsn')
cortextofsn.connect()

weightctxd1 = ctxd1pars['weight']*b2.nsiemens
cortextod1 = b2.Synapses(ctxford1, D1, delay=ctxd1pars['delay']*b2.ms, on_pre='g_e += weightctxd1')
cortextod1.connect()

weightctxd2 = ctxd2pars['weight']*b2.nsiemens
cortextod2 = b2.Synapses(ctxford2, D2, delay=ctxd2pars['delay']*b2.ms, on_pre='g_e += weightctxd2')
cortextod2.connect()

weightctxstn = ctxstnpars['weight']*b2.nsiemens
cortextostn = b2.Synapses(ctxforstn, STN, delay=ctxstnpars['delay']*b2.ms, on_pre='g_e += weightctxstn')
cortextostn.connect()

weightctxgpti = ctxgptipars['weight']*b2.nsiemens
cortextogpti = b2.Synapses(ctxforgpti, GPTI, delay=ctxgptipars['delay']*b2.ms, on_pre='g_e += weightctxgpti')
cortextogpti.connect()

weightctxgpta = ctxgptapars['weight']*b2.nsiemens
cortextogpta = b2.Synapses(ctxforgpta, GPTA, delay=ctxgptapars['delay']*b2.ms, on_pre='g_e += weightctxgpta')
cortextogpta.connect()

weightctxgpi = ctxgpipars['weight']*b2.nsiemens
cortextogpi = b2.Synapses(ctxforgpi, GPI, delay=ctxgpipars['delay']*b2.ms, on_pre='g_e += weightctxgpi')
cortextogpi.connect()