""" Parameters for my model
"""
import brian2 as b2
import random as ran

N_GPe = 153 # In realtà 152
N_GPe_B = int(N_GPe * 0.85)
N_GPe_A = int(N_GPe * 0.0405)
N_GPe_C = int(N_GPe * 0.1095)
N_STN = 45 # In realtà 44
N_STN_RB = int(N_STN * 0.6)
N_STN_LLRS = int(N_STN * 0.25)
N_STN_NR = int(N_STN * 0.15)
N_input = 1000

deft = b2.defaultclock.dt
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
p_CTX_STN = 0.03


""" Cortical Input
"""
t_recorded = b2.arange(int(duration/deft))*deft
freq = 0.06*1/b2.ms
amplit = 7.*b2.Hz
f_spon = 3.*b2.Hz
phi = ran.uniform(0,2.*b2.pi)
input_rates = b2.TimedArray(amplit*b2.cos(2.*b2.pi*freq*t_recorded + phi) + f_spon, dt = deft)
lambda_ctx_stn = 2.5*b2.ms
G_ctx_stn = 0.388*b2.nsiemens
E_ctx_stn = 0*b2.mV
tau_ctx_stn_ampa = 2.*b2.ms
tau_ctx_stn_nmda = 100.*b2.ms

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
tau_stn_gpe_ampa = 2.*b2.ms
tau_stn_gpe_nmda = 100.*b2.ms
