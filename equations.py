""" ATTENZIONE: qua dovrai fare una modifica per simulare lo stato
    patologico del Parkinson, in particolare devi aggiungere alle correnti
    Dop1 e Dop2, due parametri che vanno a modificare il valore della corrente.

    Dop1 = Dop2 = 0.8

    Guarda il codice di Fountas.
    In model.py trovi per quali NeuronGroup bisogna aggiungere questi parametri.
    In equations.py trovi invece il modo in cui Fountas li inserisce nelle equazioni.
"""

""" Equations for NeuronGroups and Synapses
"""
from brian2 import *

""" Heaviside function
"""
H = core.functions.DEFAULT_FUNCTIONS['int']
adimvolt = 1/mV # I need this to make v_rest_STN2 - v adimensional, else Dimension Mismatch error will pop up.


""" Populations of STN
"""
eqs_STN = '''
dv/dt = (1/CSTN)*(kSTN*(v - v_rest_STN1)*(v - v_thres_STN)*nS/mV - u1*pF - w2*u2*pF + I_tot) + sigma_stn*xi*mV/ms**.5 : volt
du1/dt = aSTN1*(bSTN1*(v - v_rest_STN1) - u1) : volt/second
du2/dt = aSTN2*(bSTN2*H( adimvolt*(v_rest_STN2 - v) >= 0)*(v - v_rest_STN2) - u2) : volt/second

CSTN : farad
v_peak_STN : volt
v_thres_STN : volt
v_rest_STN1 : volt
v_rest_STN2 : volt
kSTN : 1
aSTN1 : 1/second
aSTN2 : 1/second
bSTN1 : 1/second
bSTN2 : 1/second
cSTN : volt
dSTN1 : volt/second
dSTN2 : volt/second
w1 : 1
w2 : 1
ISTN_ext : amp

U = 1/(w1*abs(u2)*second/volt + 1/w1) : 1

B = 1.0/(1.0+(0.28)*exp(-0.062*v/mV)) : 1

I_lfp_stn = abs((I_chem_CTX_STN)*(1.0 - 0.5*Dop2)) + abs((I_chem_GPe_STN)*(1.0 - 0.5*Dop2)) : amp

I_tot = I_syn_tot + ISTN_ext : amp

I_syn_tot = (I_chem_CTX_STN + I_chem_GPe_STN)*(1.0 - 0.5*Dop2) : amp

I_chem_CTX_STN = G_ctx_stn*gsyn_ampa_ctx_stn*(E_ctx_stn - v) + B*G_ctx_stn*0.6*gsyn_nmda_ctx_stn*(E_ctx_stn - v) : amp
dgsyn_ampa_ctx_stn/dt = -(1/tau_ctx_stn_ampa)*gsyn_ampa_ctx_stn : siemens
dgsyn_nmda_ctx_stn/dt = -(1/tau_ctx_stn_nmda)*gsyn_nmda_ctx_stn : siemens

I_chem_GPe_STN = G_gpe_stn*gsyn_gaba_gpe_stn*(E_gpe_stn - v) : amp
dgsyn_gaba_gpe_stn/dt = -(1/tau_gpe_stn)*gsyn_gaba_gpe_stn : siemens
'''


""" Populations of GPe
"""
eqs_GPe = '''
dv/dt = (1/CGPe)*(kGPe*pF/ms/mV*(v - v_rest_GPe)*(v - v_thres_GPe) - u*pF + I_tot) + sigma_GPe*xi*mV/ms**.5 : volt
du/dt = aGPe*(bGPe*(v - v_rest_GPe) - u) : volt/second

CGPe : farad
v_thres_GPe : volt
v_peak_GPe : volt
v_rest_GPe : volt
kGPe : 1
aGPe : 1/second
bGPe : 1/second
cGPe : volt
dGPe : volt/second
IGPe_ext : amp
sigma_GPe : 1

B = 1.0/(1.0+(0.28)*exp(-0.062*v/mV)) : 1

I_lfp_gpe = abs(I_chem_GPe_GPe*(1.0 - 0.5*Dop2)) + abs(I_chem_STN_GPe*(1.0 - 0.5*Dop2)) + abs(I_chem_STR_GPe*(1.0 - 0.5*Dop2)) : amp

I_tot = I_syn_tot + IGPe_ext : amp

I_syn_tot = (I_chem_GPe_GPe + I_chem_STN_GPe + I_chem_STR_GPe)*(1.0 - 0.5*Dop2) : amp

I_chem_STR_GPe = G_str_gpe*gsyn_gaba_str_gpe*(E_str_gpe - v) : amp
dgsyn_gaba_str_gpe/dt = -(1/tau_str_gpe)*gsyn_gaba_str_gpe : siemens

I_chem_GPe_GPe = G_gpe_gpe*gsyn_gaba_gpe_gpe*(E_gpe_gpe - v) : amp
dgsyn_gaba_gpe_gpe/dt = -(1/tau_gpe_gpe)*gsyn_gaba_gpe_gpe : siemens

I_chem_STN_GPe = G_stn_gpe*gsyn_ampa_stn_gpe*(E_stn_gpe - v) + B*G_stn_gpe*0.36*gsyn_nmda_stn_gpe*(E_stn_gpe - v) : amp
dgsyn_ampa_stn_gpe/dt = -(1/tau_stn_gpe_ampa)*gsyn_ampa_stn_gpe : siemens
dgsyn_nmda_stn_gpe/dt = -(1/tau_stn_gpe_nmda)*gsyn_nmda_stn_gpe : siemens
'''
