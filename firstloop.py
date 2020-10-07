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
CSTN = 23*pF
CGPe = 68*pF
v_thres_STN = -41.4*mV
v_thres_GPe = -43*mV
v_rest_STN1 = -56.2*mV
v_rest_STN2 = -60*mV
v_rest_GPe = -52 mV
kSTN = 0.105
aSTN1 = 0.021
aSTN2 = 0.123
bSTN1 = 4
bSTN2 = 0.015
cSTN = -47.7*mV
dSTN1 = 17.1
dSTN2 = -68.4
w1 = 0.1
w2 = 0


""" The model proposed is inspired by Izhikevich 2003/2007a.
    In this model v represents the membrane voltage while
    u is an abstract recovery variable.
"""
eqs_STN = '''
dv/dt = (1/CSTN)*(kSTN*(v - v_rest_STN)(v - v_thres_STN) - u1 - w2*u2 + I + CSTN*xi) : 1
du1/dt = aSTN1*(bSTN1*(v - v_rest_STN1) - u1) : 1
du2/dt = aSTN2*(bSTN2*(v - v_rest_STN2) - u2) : 1

'''
eqs_GPe = '''
dv/dt = (1/CGPe)*(kGPe*(v - v_rest_GPe)(v - v_thres_GPe) - u + I + CGPe*xi) : 1
du/dt = aGPe*(bGPe*(v - v_rest_GPe) - u) : 1
'''
