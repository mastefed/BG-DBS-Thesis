""" This is the code needed to simulate
    the GPe-STN Loop. Here I'm using the
    Brian2 framework.
"""

import brian2 as b2

N_GPe = 153
N_STN = 45
duration = 1000*b2.ms

""" I'm gonne choose the parameters
    used by Fountas. I chose the first channel.
    This is due to the majority of first channel
    type of neurons in STN.
"""

CSTN = 23.*b2.pfarad
CGPe = 68.*b2.pfarad
sigma = 1.*b2.mV/b2.msecond**0.5
v_thres_STN = -41.4*b2.mV
v_thres_GPe = -44.*b2.mV
v_rest_STN1 = -56.2*b2.mV
v_rest_STN2 = -60.*b2.mV
v_rest_GPe = -53.*b2.mV
kSTN = 0.105 * b2.pamp / b2.mV ** 2.
aSTN1 = 0.021*(1/b2.msecond)
aSTN2 = 0.123*(1/b2.msecond)
bSTN1 = 4.*(1/b2.Gohm)
bSTN2 = 0.015
cSTN = -47.7*b2.mV
dSTN1 = 17.1*b2.pamp
dSTN2 = -68.4*b2.mV
w1 = 0.1*(1/b2.mV)
w2 = 0.*b2.nsiemens
w3 = 10.
ISTN_ext = 56.1*b2.pamp
# ISTN_ext = 1.*b2.namp

""" I'm choosing the B type among the GPe neurons.
    This is only due to them being the majority.
"""
kGPe = 0.943 * b2.pamp / b2.mV ** 2.
aGPe = 0.0045*(1/b2.msecond)
bGPe = 3.895*(1/b2.Gohm)
cGPe = -58.36*b2.mV
dGPe = 0.353*b2.pamp
IGPe_ext = 64*b2.pamp

""" Synaptic characteristics from connectivity
    probabilities to synapses' parameters.
"""
p_GPe_GPe = 0.1
p_GPe_STN = 0.1
p_STN_GPe = 0.3

""" GPe to GPe
    Chemical
"""
lambda_gpe_gpe = 1.*b2.ms
G_gpe_gpe = 0.765*b2.nsiemens
E_gpe_gpe = -65.*b2.mV
tau_gpe_gpe = 5.*b2.ms

""" GPe to STN
    Chemical
"""
lambda_gpe_stn = 4.*b2.ms
G_gpe_stn = 0.518*b2.nsiemens
E_gpe_stn = -64.*b2.mV
tau_gpe_stn = 8.*b2.ms

""" STN to GPe
    Chemical
"""
lambda_stn_gpe = 2.*b2.ms
G_stn_gpe = 1.447*b2.nsiemens
E_stn_gpe = 0.*b2.mV
tau_stn_gpe = 2.*b2.ms

""" Heaviside function
"""
H = b2.core.functions.DEFAULT_FUNCTIONS['int']
adimvolt = 1/b2.mV # I need this to make v_rest_STN2 - v adimensional, else Dimension Mismatch error will pop up.

""" The model proposed is inspired by Izhikevich 2003/2007a.
    In this model v represents the membrane voltage while
    u is an abstract recovery variable.
"""
eqs_STN = '''
dv/dt = (1/CSTN)*(kSTN*(v - v_rest_STN1)*(v - v_thres_STN) - u1 - w2*u2 + ISTN_ext + I_syn + sigma*CSTN*xi) : volt
du1/dt = aSTN1*(bSTN1*(v - v_rest_STN1) - u1) : volt/ohm
du2/dt = aSTN2*(bSTN2*H( adimvolt*(v_rest_STN2 - v) >= 0)*(v - v_rest_STN2) - u2) : volt
U = 1/(w1*abs(u2)+w3) : 1
I_syn : amp
'''
eqs_GPe = '''
dv/dt = (1/CGPe)*(kGPe*(v - v_rest_GPe)*(v - v_thres_GPe) - u + IGPe_ext + I_syn + sigma*CGPe*xi) : volt
du/dt = aGPe*(bGPe*(v - v_rest_GPe) - u) : volt/ohm
I_syn : amp
'''

STNGroup = b2.NeuronGroup(N_STN, eqs_STN, threshold='v>v_thres_STN+U*u2', reset='v=cSTN-U*u2;u1=u1+dSTN1;u2=u2+dSTN2',
                          method='euler')

GPeGroup = b2.NeuronGroup(N_GPe, eqs_GPe, threshold='v>v_thres_GPe', reset='v=cGPe;u=u+dGPe', method='euler')

""" GPe to GPe synapses
"""
eqsGPeGPe = """
I_chem_GPe_GPe = G_gpe_gpe*gsyn*(E_gpe_gpe - v) : amp
dgsyn/dt = -(1/tau_gpe_gpe)*gsyn : 1 (event-driven)
"""
ChemicalGPeGPe = b2.Synapses(GPeGroup, GPeGroup, delay=lambda_gpe_gpe, model=eqsGPeGPe,
                             on_pre="I_syn+=I_chem_GPe_GPe")
ChemicalGPeGPe.connect(True, p=p_GPe_GPe)

""" GPe to STN synapses
"""
eqsGPeSTN = """
I_chem_GPe_STN = G_gpe_stn*gsyn*(E_gpe_stn - v) : amp
dgsyn/dt = -(1/tau_gpe_stn)*gsyn : 1 (event-driven)
"""
ChemicalGPeSTN = b2.Synapses(GPeGroup, STNGroup, delay=lambda_gpe_stn, model=eqsGPeSTN,
                            on_pre="I_syn+=I_chem_GPe_STN")
ChemicalGPeSTN.connect(True, p=p_GPe_STN)

""" STN to GPe synapses
"""
eqsSTNGPe = """
I_chem_STN_GPe = G_stn_gpe*gsyn*(E_stn_gpe - v) : amp
dgsyn/dt = -(1/tau_stn_gpe)*gsyn : 1 (event-driven)
"""
ChemicalSTNGPe = b2.Synapses(STNGroup, GPeGroup,delay=lambda_stn_gpe, model=eqsSTNGPe,
                            on_pre="I_syn+=I_chem_STN_GPe")
ChemicalSTNGPe.connect(True, p=p_STN_GPe)

""" Functions to monitor neurons' state
"""
spikemonitorSTN = b2.SpikeMonitor(STNGroup, variables=['v'])
statemonitorSTN = b2.StateMonitor(STNGroup, 'v', record=True)
spikemonitorGPe = b2.SpikeMonitor(GPeGroup, variables=['v'])
statemonitorGPe = b2.StateMonitor(GPeGroup, 'v', record=True)

""" Run the code!
"""
b2.run(duration)

""" Plotting STN stuff
"""
b2.plt.figure("Membrane potential")
b2.plt.title("Membrane potential of one neuron (red = STN) (green = GPe)")
b2.plt.ylabel("Neuron membrane voltage")
b2.plt.xlabel("Time (ms)")
plotSSTN = b2.plt.plot(statemonitorSTN.t/b2.ms, statemonitorSTN.v[10]/b2.mV, 'r')

b2.plt.figure("Spikes")
b2.plt.title("Raster plot (red = STN) (green = GPe)")
b2.plt.ylabel("Neuron Index")
b2.plt.xlabel("Time (ms)")
# b2.plt.xlim((0,120))
plotMSTN = b2.plt.plot(spikemonitorSTN.t/b2.ms, spikemonitorSTN.i, 'r.',ms='1')

""" Plotting GPe stuff
"""
b2.plt.figure("Membrane potential")
b2.plt.title("Membrane potential of one neuron (red = STN) (green = GPe)")
b2.plt.ylabel("Neuron membrane voltage")
b2.plt.xlabel("Time (ms)")
b2.plt.legend()
plotSGPe = b2.plt.plot(statemonitorGPe.t/b2.ms, statemonitorGPe.v[10]/b2.mV, 'g')

b2.plt.figure("Spikes")
b2.plt.title("Raster plot (red = STN) (green = GPe)")
b2.plt.ylabel("Neuron Index")
b2.plt.xlabel("Time (ms)")
# b2.plt.xlim((0,120))
plotMGPe = b2.plt.plot(spikemonitorGPe.t/b2.ms, spikemonitorGPe.i, 'g.',ms='1')

b2.plt.show()













