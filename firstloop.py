""" This is the code needed to simulate
    the GPe-STN Loop. Here I'm using the
    Brian2 framework.
"""

import brian2 as b2

N_GPe = 153
N_GPe_A = N_GPe * 0.85
N_GPe_B = N_GPe * 0.0405
N_GPe_C = N_GPe * 0.1095
N_STN = 45
N_STN_RB = N_STN * 0.6
N_STN_LLRS = N_STN * 0.6
N_STN_NR = N_STN * 0.6
duration = 1000*b2.ms
sigma = 1.*b2.mV/b2.msecond**0.5

""" STN RB Neurons 
"""

CSTN_RB = 23.*b2.pfarad
v_peak_STN_RB = 15.4*b2.mV
v_thres_STN_RB = -41.4*b2.mV
v_rest_STN1_RB = -56.2*b2.mV
v_rest_STN2_RB = -60.*b2.mV
kSTN_RB = 0.439 * b2.pamp / b2.mV ** 2.
aSTN1_RB = 0.021*(1/b2.msecond)
aSTN2_RB = 0.123*(1/b2.msecond)
bSTN1_RB = 4.*(1/b2.Gohm)
bSTN2_RB = 0.015
cSTN_RB = -47.7*b2.mV
dSTN1_RB = 17.1*b2.pamp
dSTN2_RB = -68.4*b2.mV
w1_RB = 0.1*(1/b2.mV)
w2_RB = 0.*b2.nsiemens
w3_RB = 10.
ISTN_ext_RB = 56.1*b2.pamp

""" STN LLRS Neurons 
"""

CSTN_LLRS = 40.*b2.pfarad
v_peak_STN_LLRS = 15.4*b2.mV
v_thres_STN_LLRS = -50.*b2.mV
v_rest_STN1_LLRS = -56.2*b2.mV
v_rest_STN2_LLRS = -60.*b2.mV
kSTN_LLRS = 0.3 * b2.pamp / b2.mV ** 2.
aSTN1_LLRS = 0.05*(1/b2.msecond)
aSTN2_LLRS = 0.001*(1/b2.msecond)
bSTN1_LLRS = 0.2*(1/b2.Gohm)
bSTN2_LLRS = 0.3
cSTN_LLRS = -60.*b2.mV
dSTN1_LLRS = 1*b2.pamp
dSTN2_LLRS = 10*b2.mV
w1_LLRS = 0.01*(1/b2.mV)
w2_LLRS = 0.*b2.nsiemens
w3_LLRS = 100.
ISTN_ext_LLRS = 8.*b2.pamp

""" STN NR Neurons 
"""

CSTN_NR = 23.*b2.pfarad
v_peak_STN_NR = 15.4*b2.mV
v_thres_STN_NR = -43.75*b2.mV
v_rest_STN1_NR = -58.5*b2.mV
v_rest_STN2_NR = -43.2*b2.mV
kSTN_NR = 0.105 * b2.pamp / b2.mV ** 2.
aSTN1_NR = 0.44*(1/b2.msecond)
aSTN2_NR = 0.32*(1/b2.msecond)
bSTN1_NR = -1.35*(1/b2.Gohm)
bSTN2_NR = 3.13
cSTN_NR = -52.34*b2.mV
dSTN1_NR = 17.65*b2.pamp
dSTN2_NR = 92*b2.mV
w1_NR = 0.001*(1/b2.mV)
w2_NR = 1.*b2.nsiemens
w3_NR = 1000.
ISTN_ext_NR = -18.*b2.pamp

""" The three populations of GPe
"""
CGPe_A = 55.*b2.pfarad
v_thres_GPe_A = -42.*b2.mV
v_peak_GPe_A = 38.*b2.mV
v_rest_GPe_A = -50.7*b2.mV
kGPe_A = 0.06 * b2.pamp / b2.mV ** 2.
aGPe_A = 0.29*(1/b2.msecond)
bGPe_A = 4.26*(1/b2.Gohm)
cGPe_A = -57.4*b2.mV
dGPe_A = 110*b2.pamp
IGPe_ext_A = 167*b2.pamp

CGPe_B = 68.*b2.pfarad
v_thres_GPe_B = -44.*b2.mV
v_peak_GPe_B = 25.*b2.mV
v_rest_GPe_B = -53.*b2.mV
kGPe_B = 0.943 * b2.pamp / b2.mV ** 2.
aGPe_B = 0.0045*(1/b2.msecond)
bGPe_B = 3.895*(1/b2.Gohm)
cGPe_B = -58.36*b2.mV
dGPe_B = 0.353*b2.pamp
IGPe_ext_B = 64*b2.pamp

CGPe_C = 57.*b2.pfarad
v_thres_GPe_C = -43.*b2.mV
v_peak_GPe_C = 34.5*b2.mV
v_rest_GPe_C = -54.*b2.mV
kGPe_C = 0.099 * b2.pamp / b2.mV ** 2.
aGPe_C = 0.42*(1/b2.msecond)
bGPe_C = 7*(1/b2.Gohm)
cGPe_C = -52.*b2.mV
dGPe_C = 166*b2.pamp
IGPe_ext_C = 237.5*b2.pamp

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

""" RB, LLRS and NR populations of STN
"""
eqs_STN_RB = '''
dv/dt = (1/CSTN_RB)*(kSTN_RB*(v - v_rest_STN1_RB)*(v - v_thres_STN_RB) - u1 - w2_RB*u2 + ISTN_ext_RB + I_syn + sigma*CSTN_RB*xi) : volt
du1/dt = aSTN1_RB*(bSTN1_RB*(v - v_rest_STN1_RB) - u1) : volt/ohm
du2/dt = aSTN2_RB*(bSTN2_RB*H( adimvolt*(v_rest_STN2_RB - v) >= 0)*(v - v_rest_STN2_RB) - u2) : volt
U = 1/(w1_RB*abs(u2)+w3_RB) : 1
I_syn : amp
'''

eqs_STN_LLRS = '''
dv/dt = (1/CSTN_LLRS)*(kSTN_LLRS*(v - v_rest_STN1_LLRS)*(v - v_thres_STN_LLRS) - u1 - w2_LLRS*u2 + ISTN_ext_LLRS + I_syn + sigma*CSTN_LLRS*xi) : volt
du1/dt = aSTN1_LLRS*(bSTN1_LLRS*(v - v_rest_STN1_LLRS) - u1) : volt/ohm
du2/dt = aSTN2_LLRS*(bSTN2_LLRS*H( adimvolt*(v_rest_STN2_LLRS - v) >= 0)*(v - v_rest_STN2_LLRS) - u2) : volt
U = 1/(w1_LLRS*abs(u2)+w3_LLRS) : 1
I_syn : amp
'''

eqs_STN_NR = '''
dv/dt = (1/CSTN_NR)*(kSTN_NR*(v - v_rest_STN1_NR)*(v - v_thres_STN_NR) - u1 - w2_NR*u2 + ISTN_ext_NR + I_syn + sigma*CSTN_NR*xi) : volt
du1/dt = aSTN1_NR*(bSTN1_NR*(v - v_rest_STN1_NR) - u1) : volt/ohm
du2/dt = aSTN2_NR*(bSTN2_NR*H( adimvolt*(v_rest_STN2_NR - v) >= 0)*(v - v_rest_STN2_NR) - u2) : volt
U = 1/(w1_NR*abs(u2)+w3_NR) : 1
I_syn : amp
'''

""" A,B and C populations of GPe
"""
eqs_GPe_A = '''
dv/dt = (1/CGPe_A)*(kGPe_A*(v - v_rest_GPe_A)*(v - v_thres_GPe_A) - u + IGPe_ext_A + I_syn + sigma*CGPe_A*xi) : volt
du/dt = aGPe_A*(bGPe_A*(v - v_rest_GPe_A) - u) : volt/ohm
I_syn : amp
'''

eqs_GPe_B = '''
dv/dt = (1/CGPe_B)*(kGPe_B*(v - v_rest_GPe_B)*(v - v_thres_GPe_B) - u + IGPe_ext_B + I_syn + sigma*CGPe_B*xi) : volt
du/dt = aGPe_B*(bGPe_B*(v - v_rest_GPe_B) - u) : volt/ohm
I_syn : amp
'''

eqs_GPe_C = '''
dv/dt = (1/CGPe_C)*(kGPe_C*(v - v_rest_GPe_C)*(v - v_thres_GPe_C) - u + IGPe_ext_C + I_syn + sigma*CGPe_C*xi) : volt
du/dt = aGPe_C*(bGPe_C*(v - v_rest_GPe_C) - u) : volt/ohm
I_syn : amp
'''


""" All the populations' NeuronGroup, first the STN ones and then the GPe ones
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


""" GPe to GPe synapses
"""
eqsGPeGPe = """
I_chem_GPe_GPe = G_gpe_gpe*gsyn*(E_gpe_gpe - v) : amp
dgsyn/dt = -(1/tau_gpe_gpe)*gsyn : 1 (event-driven)
"""

ChemicalGPeAGPeA = b2.Synapses(GPeAGroup, GPeAGroup, delay=lambda_gpe_gpe, model=eqsGPeGPe,
on_pre="I_syn+=I_chem_GPe_GPe")
ChemicalGPeAGPeA.connect(True, p=p_GPe_GPe)

ChemicalGPeBGPeB = b2.Synapses(GPeBGroup, GPeBGroup, delay=lambda_gpe_gpe, model=eqsGPeGPe,
on_pre="I_syn+=I_chem_GPe_GPe")
ChemicalGPeBGPeB.connect(True, p=p_GPe_GPe)

ChemicalGPeCGPeC = b2.Synapses(GPeCGroup, GPeCGroup, delay=lambda_gpe_gpe, model=eqsGPeGPe,
on_pre="I_syn+=I_chem_GPe_GPe")
ChemicalGPeCGPeC.connect(True, p=p_GPe_GPe)

ChemicalGPeAGPeB = b2.Synapses(GPeAGroup, GPeBGroup, delay=lambda_gpe_gpe, model=eqsGPeGPe,
on_pre="I_syn+=I_chem_GPe_GPe")
ChemicalGPeAGPeB.connect(True, p=p_GPe_GPe)

ChemicalGPeAGPeC = b2.Synapses(GPeAGroup, GPeCGroup, delay=lambda_gpe_gpe, model=eqsGPeGPe,
on_pre="I_syn+=I_chem_GPe_GPe")
ChemicalGPeAGPeC.connect(True, p=p_GPe_GPe)

ChemicalGPeBGPeC = b2.Synapses(GPeBGroup, GPeCGroup, delay=lambda_gpe_gpe, model=eqsGPeGPe,
on_pre="I_syn+=I_chem_GPe_GPe")
ChemicalGPeBGPeC.connect(True, p=p_GPe_GPe)

ChemicalGPeCGPeB = b2.Synapses(GPeCGroup, GPeBGroup, delay=lambda_gpe_gpe, model=eqsGPeGPe,
on_pre="I_syn+=I_chem_GPe_GPe")
ChemicalGPeCGPeB.connect(True, p=p_GPe_GPe)

ChemicalGPeBGPeA = b2.Synapses(GPeBGroup, GPeAGroup, delay=lambda_gpe_gpe, model=eqsGPeGPe,
on_pre="I_syn+=I_chem_GPe_GPe")
ChemicalGPeBGPeA.connect(True, p=p_GPe_GPe)

ChemicalGPeCGPeA = b2.Synapses(GPeCGroup, GPeAGroup, delay=lambda_gpe_gpe, model=eqsGPeGPe,
on_pre="I_syn+=I_chem_GPe_GPe")
ChemicalGPeCGPeA.connect(True, p=p_GPe_GPe)



""" GPe to STN synapses
"""
eqsGPeSTN = """
I_chem_GPe_STN = G_gpe_stn*gsyn*(E_gpe_stn - v) : amp
dgsyn/dt = -(1/tau_gpe_stn)*gsyn : 1 (event-driven)
"""
# A to RB/LLRS/NR
ChemicalGPeASTNRB = b2.Synapses(GPeAGroup, STNRBGroup, delay=lambda_gpe_stn, model=eqsGPeSTN,
on_pre="I_syn+=I_chem_GPe_STN")
ChemicalGPeASTNRB.connect(True, p=p_GPe_STN)

ChemicalGPeASTNLLRS = b2.Synapses(GPeAGroup, STNLLRSGroup, delay=lambda_gpe_stn, model=eqsGPeSTN,
on_pre="I_syn+=I_chem_GPe_STN")
ChemicalGPeASTNLLRS.connect(True, p=p_GPe_STN)

ChemicalGPeASTNNR = b2.Synapses(GPeAGroup, STNRBGroup, delay=lambda_gpe_stn, model=eqsGPeSTN,
on_pre="I_syn+=I_chem_GPe_STN")
ChemicalGPeASTNNR.connect(True, p=p_GPe_STN)

# A to RB/LLRS/NR
ChemicalGPeBSTNRB = b2.Synapses(GPeBGroup, STNRBGroup, delay=lambda_gpe_stn, model=eqsGPeSTN,
on_pre="I_syn+=I_chem_GPe_STN")
ChemicalGPeBSTNRB.connect(True, p=p_GPe_STN)

ChemicalGPeBSTNLLRS = b2.Synapses(GPeBGroup, STNLLRSGroup, delay=lambda_gpe_stn, model=eqsGPeSTN,
on_pre="I_syn+=I_chem_GPe_STN")
ChemicalGPeBSTNLLRS.connect(True, p=p_GPe_STN)

ChemicalGPeBSTNNR = b2.Synapses(GPeBGroup, STNRBGroup, delay=lambda_gpe_stn, model=eqsGPeSTN,
on_pre="I_syn+=I_chem_GPe_STN")
ChemicalGPeBSTNNR.connect(True, p=p_GPe_STN)

# C to RB/LLRS/NR
ChemicalGPeCSTNRB = b2.Synapses(GPeCGroup, STNRBGroup, delay=lambda_gpe_stn, model=eqsGPeSTN,
on_pre="I_syn+=I_chem_GPe_STN")
ChemicalGPeCSTNRB.connect(True, p=p_GPe_STN)

ChemicalGPeCSTNLLRS = b2.Synapses(GPeCGroup, STNLLRSGroup, delay=lambda_gpe_stn, model=eqsGPeSTN,
on_pre="I_syn+=I_chem_GPe_STN")
ChemicalGPeCSTNLLRS.connect(True, p=p_GPe_STN)

ChemicalGPeCSTNNR = b2.Synapses(GPeCGroup, STNRBGroup, delay=lambda_gpe_stn, model=eqsGPeSTN,
on_pre="I_syn+=I_chem_GPe_STN")
ChemicalGPeCSTNNR.connect(True, p=p_GPe_STN)




""" STN to GPe synapses
"""
eqsSTNGPe = """
I_chem_STN_GPe = G_stn_gpe*gsyn*(E_stn_gpe - v) : amp
dgsyn/dt = -(1/tau_stn_gpe)*gsyn : 1 (event-driven)
"""

# RB to A/B/C
ChemicalSTNRBGPeA = b2.Synapses(STNRBGroup, GPeAGroup,delay=lambda_stn_gpe, model=eqsSTNGPe,
on_pre="I_syn+=I_chem_STN_GPe")
ChemicalSTNRBGPeA.connect(True, p=p_STN_GPe)

ChemicalSTNRBGPeB = b2.Synapses(STNRBGroup, GPeBGroup,delay=lambda_stn_gpe, model=eqsSTNGPe,
on_pre="I_syn+=I_chem_STN_GPe")
ChemicalSTNRBGPeB.connect(True, p=p_STN_GPe)

ChemicalSTNRBGPeC = b2.Synapses(STNRBGroup, GPeCGroup,delay=lambda_stn_gpe, model=eqsSTNGPe,
on_pre="I_syn+=I_chem_STN_GPe")
ChemicalSTNRBGPeC.connect(True, p=p_STN_GPe)

# LLRS to A/B/C
ChemicalSTNLLRSGPeA = b2.Synapses(STNLLRSGroup, GPeAGroup,delay=lambda_stn_gpe, model=eqsSTNGPe,
on_pre="I_syn+=I_chem_STN_GPe")
ChemicalSTNLLRSGPeA.connect(True, p=p_STN_GPe)

ChemicalSTNLLRSGPeB = b2.Synapses(STNLLRSGroup, GPeBGroup,delay=lambda_stn_gpe, model=eqsSTNGPe,
on_pre="I_syn+=I_chem_STN_GPe")
ChemicalSTNLLRSGPeB.connect(True, p=p_STN_GPe)

ChemicalSTNLLRSGPeC = b2.Synapses(STNLLRSGroup, GPeCGroup,delay=lambda_stn_gpe, model=eqsSTNGPe,
on_pre="I_syn+=I_chem_STN_GPe")
ChemicalSTNLLRSGPeC.connect(True, p=p_STN_GPe)

# NR to A/B/C
ChemicalSTNNRGPeA = b2.Synapses(STNNRGroup, GPeAGroup,delay=lambda_stn_gpe, model=eqsSTNGPe,
on_pre="I_syn+=I_chem_STN_GPe")
ChemicalSTNNRGPeA.connect(True, p=p_STN_GPe)

ChemicalSTNNRGPeB = b2.Synapses(STNNRGroup, GPeBGroup,delay=lambda_stn_gpe, model=eqsSTNGPe,
on_pre="I_syn+=I_chem_STN_GPe")
ChemicalSTNNRGPeB.connect(True, p=p_STN_GPe)

ChemicalSTNNRGPeC = b2.Synapses(STNNRGroup, GPeCGroup,delay=lambda_stn_gpe, model=eqsSTNGPe,
on_pre="I_syn+=I_chem_STN_GPe")
ChemicalSTNNRGPeC.connect(True, p=p_STN_GPe)


""" Functions to monitor neurons' state
"""
spikemonitorSTNRB = b2.SpikeMonitor(STNRBGroup, variables=['v'])
statemonitorSTNRB = b2.StateMonitor(STNRBGroup, 'v', record=True)

spikemonitorSTNLLRS = b2.SpikeMonitor(STNLLRSGroup, variables=['v'])
statemonitorSTNLLRS = b2.StateMonitor(STNLLRSGroup, 'v', record=True)

spikemonitorSTNNR = b2.SpikeMonitor(STNNRGroup, variables=['v'])
statemonitorSTNNR = b2.StateMonitor(STNNRGroup, 'v', record=True)

spikemonitorGPeA = b2.SpikeMonitor(GPeAGroup, variables=['v'])
statemonitorGPeA = b2.StateMonitor(GPeAGroup, 'v', record=True)

spikemonitorGPeB = b2.SpikeMonitor(GPeBGroup, variables=['v'])
statemonitorGPeB = b2.StateMonitor(GPeBGroup, 'v', record=True)

spikemonitorGPeC = b2.SpikeMonitor(GPeCGroup, variables=['v'])
statemonitorGPeC = b2.StateMonitor(GPeCGroup, 'v', record=True)


""" Run the code!
"""
b2.run(duration)

""" Plotting STN stuff
"""
b2.plt.figure("Membrane potential STN")
b2.plt.title("Membrane potential of one neuron (red = STN RB) (green = STN LLRS) (blue = STN NR)")
b2.plt.ylabel("Neuron membrane voltage")
b2.plt.xlabel("Time (ms)")
plotSSTNNR = b2.plt.plot(statemonitorSTNNR.t/b2.ms, statemonitorSTNNR.v[0]/b2.mV, 'b')
plotSSTNLLRS = b2.plt.plot(statemonitorSTNLLRS.t/b2.ms, statemonitorSTNLLRS.v[0]/b2.mV, 'g')
plotSSTNRB = b2.plt.plot(statemonitorSTNRB.t/b2.ms, statemonitorSTNRB.v[0]/b2.mV, 'r')

b2.plt.figure("Spikes STN")
b2.plt.title("Raster plot (red = STN RB) (green = STN LLRS) (blue = STN NR)")
b2.plt.ylabel("Neuron Index")
b2.plt.xlabel("Time (ms)")
b2.plt.ylim((0,45))
plotMSTNRB = b2.plt.plot(spikemonitorSTNRB.t/b2.ms, spikemonitorSTNRB.i, 'r.',ms='2')
plotMSTNLLRS = b2.plt.plot(spikemonitorSTNLLRS.t/b2.ms, spikemonitorSTNLLRS.i, 'g.',ms='2')
plotMSTNNR = b2.plt.plot(spikemonitorSTNNR.t/b2.ms, spikemonitorSTNNR.i, 'b.',ms='2')




""" Plotting GPe stuff
"""
b2.plt.figure("Membrane potential GPe")
b2.plt.title("Membrane potential of one neuron (red = GPe A) (green = GPe B) (blue = GPe C)")
b2.plt.ylabel("Neuron membrane voltage")
b2.plt.xlabel("Time (ms)")
plotSGPeA = b2.plt.plot(statemonitorGPeA.t/b2.ms, statemonitorGPeA.v[0]/b2.mV, 'r')
plotSGPeB = b2.plt.plot(statemonitorGPeB.t/b2.ms, statemonitorGPeB.v[0]/b2.mV, 'g')
plotSGPeC = b2.plt.plot(statemonitorGPeC.t/b2.ms, statemonitorGPeC.v[0]/b2.mV, 'b')

b2.plt.figure("Spikes GPe")
b2.plt.title("Raster plot (red = GPe A) (green = GPe B) (blue = GPe C)")
b2.plt.ylabel("Neuron Index")
b2.plt.xlabel("Time (ms)")
b2.plt.ylim((0,153))
plotMGPeA = b2.plt.plot(spikemonitorGPeA.t/b2.ms, spikemonitorGPeA.i, 'r.',ms='2')
plotMGPeB = b2.plt.plot(spikemonitorGPeB.t/b2.ms, spikemonitorGPeB.i, 'g.',ms='2')
plotMGPeC = b2.plt.plot(spikemonitorGPeC.t/b2.ms, spikemonitorGPeC.i, 'b.',ms='2')

b2.plt.show()

""" T = [26.31; 3.33]
oscillazioni nella frequenza beta
"""