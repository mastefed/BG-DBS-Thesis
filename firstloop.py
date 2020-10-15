""" This is the code needed to simulate
    the GPe-STN Loop. Here I'm using the
    Brian2 framework.
"""

import brian2 as b2

N_GPe = 153
N_STN = 45

""" I'm gonne choose the parameters
    used by Fountas. I chose the first channel.
    This is due to the majority of first channel
    type of neurons in STN.
"""
CSTN = 23*b2.pfarad
CGPe = 68*b2.pfarad
v_thres_STN = -41.4*b2.mV
v_thres_GPe = -44*b2.mV
v_rest_STN1 = -56.2*b2.mV
v_rest_STN2 = -60*b2.mV
v_rest_GPe = -53*b2.mV
kSTN = 0.105
aSTN1 = 0.021
aSTN2 = 0.123
bSTN1 = 4
bSTN2 = 0.015
cSTN = -47.7*b2.mV
dSTN1 = 17.1
dSTN2 = -68.4
w1 = 0.1
w2 = 0
ISTN = 56.1*b2.pamp

""" I'm choosing the B type among the GPe neurons.
    This is only due to them being the majority.
"""
kGPe = 0.943
aGPe = 0.0045
bGPe = 3.895
cGPe = -58.36*b2.mV
dGPe = 0.353 
IGPe = 64*b2.pamp

""" Synaptic characteristics from connectivity
    probabilities to synapses' parameters.
"""
p_GPe_GPe = 0.1
p_GPe_STN = 0.1
p_STN_GPe = 0.3

""" GPe to GPe
    Chemical
"""
lambda_gpe_gpe = 1*b2.ms
G_gpe_gpe = 0.765*b2.nsiemens
E_gpe_gpe = -65*b2.mV
tau_gpe_gpe = 5*b2.ms

""" GPe to STN
    Chemical
"""
lambda_gpe_stn = 4*b2.ms
G_gpe_stn = 0.518*b2.nsiemens
E_gpe_stn = -64*b2.mV
tau_gpe_stn = 8*b2.ms

""" STN to GPe
    Chemical
"""
lambda_stn_gpe = 2*b2.ms
G_stn_gpe = 1.447*b2.nsiemens
E_stn_gpe = 0*b2.mV
tau_stn_gpe = 2*b2.ms

""" The model proposed is inspired by Izhikevich 2003/2007a.
    In this model v represents the membrane voltage while
    u is an abstract recovery variable.
"""
eqs_STN = '''
dv/dt = (1/CSTN)*(kSTN*(v - v_rest_STN)*(v - v_thres_STN) - u1 - w2*u2 + ISTN + CSTN*xi) : 1
du1/dt = aSTN1*(bSTN1*(v - v_rest_STN1) - u1) : 1
du2/dt = aSTN2*(bSTN2*(v - v_rest_STN2) - u2) : 1
U = 1/(w1*abs(u2)+1/w1) : 1
'''
eqs_GPe = '''
dv/dt = (1/CGPe)*(kGPe*(v - v_rest_GPe)*(v - v_thres_GPe) - u + IGPe + CGPe*xi) : 1
du/dt = aGPe*(bGPe*(v - v_rest_GPe) - u) : 1
'''

STNGroup = b2.NeuronGroup(N_STN, eqs_STN, threshold='v>v_thres_STN', reset='v=cSTN-U*u2;u1=u1+dSTN1;u2=u2+dSTN2', method='exact')

GPeGroup = b2.NeuronGroup(N_GPe, eqs_GPe, threshold='v>v_thres_GPe', reset='v=cGPe;u=u+dGPe', method='exact')
