""" Parameters for my model
"""
from brian2 import *
import random as ran
import numpy as np

rate_CTX = 0*Hz
rate_STR = 0*Hz

rates_CTX = np.arange(1, 40, 1)
rates_STR = np.arange(1, 40, 1)

N_GPe = 153 # In realtà 152
N_GPe_B = int(N_GPe * 0.85)
N_GPe_A = int(N_GPe * 0.0405)
N_GPe_C = int(N_GPe * 0.1095)
N_STN = 45 # In realtà 44
N_STN_RB = int(N_STN * 0.6)
N_STN_LLRS = int(N_STN * 0.25)
N_STN_NR = int(N_STN * 0.15)
N_input_CTX = 1000
N_input_MSN2 = 9207/2

deft = defaultclock.dt
duration = 10000*ms

sigma_stn = 0.5
""" STN RB Neurons 
"""
CSTN_RB = 23.*pfarad
v_peak_STN_RB = 15.4*mV
v_thres_STN_RB = -41.4*mV
v_rest_STN1_RB = -56.2*mV
v_rest_STN2_RB = -60.*mV
kSTN_RB = 0.439 
aSTN1_RB = 0.021*(1/ms)
aSTN2_RB = 0.123*(1/ms)
bSTN1_RB = 4.*(1/ms)
bSTN2_RB = 0.015/ms
cSTN_RB = -47.7*mV
dSTN1_RB = 17.1*mV/ms
dSTN2_RB = -68.4*mV/ms
w1_RB = 0.1
w2_RB = 0.
ISTN_ext_RB = 56.1*pamp

""" STN LLRS Neurons 
"""
CSTN_LLRS = 40.*pfarad
v_peak_STN_LLRS = 15.4*mV
v_thres_STN_LLRS = -50.*mV
v_rest_STN1_LLRS = -56.2*mV
v_rest_STN2_LLRS = -60.*mV
kSTN_LLRS = 0.3 
aSTN1_LLRS = 0.05*(1/ms)
aSTN2_LLRS = 0.001*(1/ms)
bSTN1_LLRS = 0.2*(1/ms)
bSTN2_LLRS = 0.3/ms
cSTN_LLRS = -60.*mV
dSTN1_LLRS = 1*mV/ms
dSTN2_LLRS = 10*mV/ms
w1_LLRS = 0.01
w2_LLRS = 0.
ISTN_ext_LLRS = 8.*pamp

""" STN NR Neurons 
"""
CSTN_NR = 23.*pfarad
v_peak_STN_NR = 15.4*mV
v_thres_STN_NR = -43.75*mV
v_rest_STN1_NR = -58.5*mV
v_rest_STN2_NR = -43.2*mV
kSTN_NR = 0.105 
aSTN1_NR = 0.44*(1/ms)
aSTN2_NR = 0.32*(1/ms)
bSTN1_NR = -1.35*(1/ms)
bSTN2_NR = 3.13/ms
cSTN_NR = -52.34*mV
dSTN1_NR = 17.65*mV/ms
dSTN2_NR = 92*mV/ms
w1_NR = 0.001
w2_NR = 1.
ISTN_ext_NR = -18.*pamp

""" The three populations of GPe
"""
sigma_gpe = 3.

CGPe_A = 55.*pfarad
v_thres_GPe_A = -42.*mV
v_peak_GPe_A = 38.*mV
v_rest_GPe_A = -50.7*mV
kGPe_A = 0.06 
aGPe_A = 0.29*(1/ms)
bGPe_A = 4.26*(1/ms)
cGPe_A = -57.4*mV
dGPe_A = 110*mV/ms
IGPe_ext_A = 167*pamp

CGPe_B = 68.*pfarad
v_thres_GPe_B = -44.*mV
v_peak_GPe_B = 25.*mV
v_rest_GPe_B = -53.*mV
kGPe_B = 0.943
aGPe_B = 0.0045*(1/ms)
bGPe_B = 3.895*(1/ms)
cGPe_B = -58.36*mV
dGPe_B = 0.353*mV/ms
IGPe_ext_B = 64*pamp

CGPe_C = 57.*pfarad
v_thres_GPe_C = -43.*mV
v_peak_GPe_C = 34.5*mV
v_rest_GPe_C = -54.*mV
kGPe_C = 0.099
aGPe_C = 0.42*(1/ms)
bGPe_C = 7*(1/ms)
cGPe_C = -52.*mV
dGPe_C = 166*mV/ms
IGPe_ext_C = 237.5*pamp

""" Synaptic characteristics from connectivity
    probabilities to synapses' parameters.
"""
p_GPe_GPe = 0.1
p_GPe_STN = 0.1
p_STN_GPe = 0.3
p_CTX_STN = 0.03
p_STR_GPe = 0.033


""" Cortical Input
"""
t_recorded = arange(int(duration/deft))*deft
freq = 0.03*1/ms
amplit = 7.*Hz
f_spon = 3.*Hz
phi = ran.uniform(0,2.*pi)
input_rates = TimedArray(amplit*cos(2.*pi*freq*t_recorded + phi) + f_spon, dt = deft)
lambda_ctx_stn = 2.5*ms
G_ctx_stn = 0.388*nsiemens
E_ctx_stn = 0*mV
tau_ctx_stn_ampa = 2.*ms
tau_ctx_stn_nmda = 100.*ms

""" Striatal Input
"""
lambda_str_gpe = 5.*ms
G_str_gpe = 5.435*nsiemens
E_str_gpe = -65.*mV
tau_str_gpe = 6.*ms

""" GPe to GPe
    Chemical
"""
lambda_gpe_gpe = 1.*ms
G_gpe_gpe = 0.765*nsiemens
E_gpe_gpe = -65.*mV
tau_gpe_gpe = 5.*ms

""" GPe to STN
    Chemical
"""
lambda_gpe_stn = 4.*ms
G_gpe_stn = 0.518*nsiemens
E_gpe_stn = -64.*mV
tau_gpe_stn = 8.*ms

""" STN to GPe
    Chemical
"""

lambda_stn_gpe = 2.*ms
G_stn_gpe = 1.447*nsiemens
E_stn_gpe = 0.*mV
tau_stn_gpe_ampa = 2.*ms
tau_stn_gpe_nmda = 100.*ms

""" Other Synaptic Parameters
"""
Dop1 = Dop2 = 0.8