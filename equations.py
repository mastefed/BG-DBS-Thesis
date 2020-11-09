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


""" RB, LLRS and NR populations of STN
"""
eqs_STN_RB = '''
dv/dt = (1/CSTN_RB)*(kSTN_RB*(v - v_rest_STN1_RB)*(v - v_thres_STN_RB)*nS/mV - u1*pF - w2_RB*u2*pF + I_tot) + sigma_stn*xi*mV/ms**.5 : volt
du1/dt = aSTN1_RB*(bSTN1_RB*(v - v_rest_STN1_RB) - u1) : volt/second
du2/dt = aSTN2_RB*(bSTN2_RB*H( adimvolt*(v_rest_STN2_RB - v) >= 0)*(v - v_rest_STN2_RB) - u2) : volt/second

U = 1/(w1_RB*abs(u2)*second/volt + 1/w1_RB) : 1

B = 1.0/(1.0+(0.28)*exp(-0.062*v/mV)) : 1

I_lfp_stnrb = abs(I_chem_CTX_STN) + abs(I_chem_GPe_STN) : amp

I_tot = I_syn_tot + ISTN_ext_RB : amp

I_syn_tot = I_chem_CTX_STN + I_chem_GPe_STN : amp

I_chem_CTX_STN = G_ctx_stn*gsyn_ampa_ctx_stn*(E_ctx_stn - v) + B*G_ctx_stn*0.6*gsyn_nmda_ctx_stn*(E_ctx_stn - v) : amp
dgsyn_ampa_ctx_stn/dt = -(1/tau_ctx_stn_ampa)*gsyn_ampa_ctx_stn : 1
dgsyn_nmda_ctx_stn/dt = -(1/tau_ctx_stn_nmda)*gsyn_nmda_ctx_stn : 1

I_chem_GPe_STN = G_gpe_stn*gsyn_gaba_gpe_stn*(E_gpe_stn - v) : amp
dgsyn_gaba_gpe_stn/dt = -(1/tau_gpe_stn)*gsyn_gaba_gpe_stn : 1
'''

eqs_STN_LLRS = '''
dv/dt = (1/CSTN_LLRS)*(kSTN_LLRS*(v - v_rest_STN1_LLRS)*(v - v_thres_STN_LLRS)*nS/mV - u1*pF - w2_LLRS*u2*pF + I_tot) + sigma_stn*xi*mV/ms**.5 : volt
du1/dt = aSTN1_LLRS*(bSTN1_LLRS*(v - v_rest_STN1_LLRS) - u1) : volt/second
du2/dt = aSTN2_LLRS*(bSTN2_LLRS*H( adimvolt*(v_rest_STN2_LLRS - v) >= 0)*(v - v_rest_STN2_LLRS) - u2) : volt/second

U = 1/(w1_LLRS*abs(u2)*second/volt+1/w1_LLRS) : 1

B = 1.0/(1.0+(0.28)*exp(-0.062*v/mV)) : 1

I_lfp_stnllrs = abs(I_chem_CTX_STN) + abs(I_chem_GPe_STN) : amp

I_tot = I_syn_tot + ISTN_ext_LLRS : amp

I_syn_tot = I_chem_CTX_STN + I_chem_GPe_STN : amp

I_chem_CTX_STN = G_ctx_stn*gsyn_ampa_ctx_stn*(E_ctx_stn - v) + B*G_ctx_stn*0.6*gsyn_nmda_ctx_stn*(E_ctx_stn - v) : amp
dgsyn_ampa_ctx_stn/dt = -(1/tau_ctx_stn_ampa)*gsyn_ampa_ctx_stn : 1
dgsyn_nmda_ctx_stn/dt = -(1/tau_ctx_stn_nmda)*gsyn_nmda_ctx_stn : 1

I_chem_GPe_STN = G_gpe_stn*gsyn_gaba_gpe_stn*(E_gpe_stn - v) : amp
dgsyn_gaba_gpe_stn/dt = -(1/tau_gpe_stn)*gsyn_gaba_gpe_stn : 1
'''

eqs_STN_NR = '''
dv/dt = (1/CSTN_NR)*(kSTN_NR*(v - v_rest_STN1_NR)*(v - v_thres_STN_NR)*nS/mV - u1*pF - w2_NR*u2*pF + I_tot) + sigma_stn*xi*mV/ms**.5 : volt
du1/dt = aSTN1_NR*(bSTN1_NR*(v - v_rest_STN1_NR) - u1) : volt/second
du2/dt = aSTN2_NR*(bSTN2_NR*H( adimvolt*(v_rest_STN2_NR - v) >= 0)*(v - v_rest_STN2_NR) - u2) : volt/second

U = 1/(w1_NR*abs(u2)*second/volt+1/w1_NR) : 1

B = 1.0/(1.0+(0.28)*exp(-0.062*v/mV)) : 1

I_lfp_stnnr = abs(I_chem_CTX_STN) + abs(I_chem_GPe_STN) : amp

I_tot = I_syn_tot + ISTN_ext_NR : amp

I_syn_tot = I_chem_CTX_STN + I_chem_GPe_STN : amp

I_chem_CTX_STN = G_ctx_stn*gsyn_ampa_ctx_stn*(E_ctx_stn - v) + B*G_ctx_stn*0.6*gsyn_nmda_ctx_stn*(E_ctx_stn - v) : amp
dgsyn_ampa_ctx_stn/dt = -(1/tau_ctx_stn_ampa)*gsyn_ampa_ctx_stn : 1
dgsyn_nmda_ctx_stn/dt = -(1/tau_ctx_stn_nmda)*gsyn_nmda_ctx_stn : 1

I_chem_GPe_STN = G_gpe_stn*gsyn_gaba_gpe_stn*(E_gpe_stn - v) : amp
dgsyn_gaba_gpe_stn/dt = -(1/tau_gpe_stn)*gsyn_gaba_gpe_stn : 1
'''

""" A,B and C populations of GPe
"""
eqs_GPe_A = '''
dv/dt = (1/CGPe_A)*(kGPe_A*pF/ms/mV*(v - v_rest_GPe_A)*(v - v_thres_GPe_A) - u*pF + I_tot) + sigma_gpe*xi*mV/ms**.5 : volt
du/dt = aGPe_A*(bGPe_A*(v - v_rest_GPe_A) - u) : volt/second

B = 1.0/(1.0+(0.28)*exp(-0.062*v/mV)) : 1

I_lfp_gpea = abs(I_chem_GPe_GPe) + abs(I_chem_STN_GPe) + abs(I_chem_STR_GPe) : amp

I_tot = I_syn_tot + IGPe_ext_A : amp

I_syn_tot = I_chem_GPe_GPe + I_chem_STN_GPe + I_chem_STR_GPe : amp

I_chem_STR_GPe = G_str_gpe*gsyn_gaba_str_gpe*(E_str_gpe - v) : amp
dgsyn_gaba_str_gpe/dt = -(1/tau_str_gpe)*gsyn_gaba_str_gpe : 1

I_chem_GPe_GPe = G_gpe_gpe*gsyn_gaba_gpe_gpe*(E_gpe_gpe - v) : amp
dgsyn_gaba_gpe_gpe/dt = -(1/tau_gpe_gpe)*gsyn_gaba_gpe_gpe : 1

I_chem_STN_GPe = G_stn_gpe*gsyn_ampa_stn_gpe*(E_stn_gpe - v) + B*G_stn_gpe*0.36*gsyn_nmda_stn_gpe*(E_stn_gpe - v) : amp
dgsyn_ampa_stn_gpe/dt = -(1/tau_stn_gpe_ampa)*gsyn_ampa_stn_gpe : 1 
dgsyn_nmda_stn_gpe/dt = -(1/tau_stn_gpe_nmda)*gsyn_nmda_stn_gpe : 1
'''

eqs_GPe_B = '''
dv/dt = (1/CGPe_B)*(kGPe_B*pF/ms/mV*(v - v_rest_GPe_B)*(v - v_thres_GPe_B) - u*pF + I_tot) + sigma_gpe*xi*mV/ms**.5 : volt
du/dt = aGPe_B*(bGPe_B*(v - v_rest_GPe_B) - u) : volt/second

B = 1.0/(1.0+(0.28)*exp(-0.062*v/mV)) : 1

I_lfp_gpeb = abs(I_chem_GPe_GPe) + abs(I_chem_STN_GPe) + abs(I_chem_STR_GPe) : amp

I_tot = I_syn_tot + IGPe_ext_B : amp

I_syn_tot = I_chem_GPe_GPe + I_chem_STN_GPe + I_chem_STR_GPe : amp

I_chem_STR_GPe = G_str_gpe*gsyn_gaba_str_gpe*(E_str_gpe - v) : amp
dgsyn_gaba_str_gpe/dt = -(1/tau_str_gpe)*gsyn_gaba_str_gpe : 1

I_chem_GPe_GPe = G_gpe_gpe*gsyn_gaba_gpe_gpe*(E_gpe_gpe - v) : amp
dgsyn_gaba_gpe_gpe/dt = -(1/tau_gpe_gpe)*gsyn_gaba_gpe_gpe : 1

I_chem_STN_GPe = G_stn_gpe*gsyn_ampa_stn_gpe*(E_stn_gpe - v) + B*G_stn_gpe*0.36*gsyn_nmda_stn_gpe*(E_stn_gpe - v) : amp
dgsyn_ampa_stn_gpe/dt = -(1/tau_stn_gpe_ampa)*gsyn_ampa_stn_gpe : 1 
dgsyn_nmda_stn_gpe/dt = -(1/tau_stn_gpe_nmda)*gsyn_nmda_stn_gpe : 1
'''

eqs_GPe_C = '''
dv/dt = (1/CGPe_C)*(kGPe_C*pF/ms/mV*(v - v_rest_GPe_C)*(v - v_thres_GPe_C) - u*pF + I_tot) + sigma_gpe*xi*mV/ms**.5 : volt
du/dt = aGPe_C*(bGPe_C*(v - v_rest_GPe_C) - u) : volt/second

B = 1.0/(1.0+(0.28)*exp(-0.062*v/mV)) : 1

I_lfp_gpec = abs(I_chem_GPe_GPe) + abs(I_chem_STN_GPe) + abs(I_chem_STR_GPe) : amp

I_tot = I_syn_tot + IGPe_ext_C : amp

I_syn_tot = I_chem_GPe_GPe + I_chem_STN_GPe + I_chem_STR_GPe : amp

I_chem_STR_GPe = G_str_gpe*gsyn_gaba_str_gpe*(E_str_gpe - v) : amp
dgsyn_gaba_str_gpe/dt = -(1/tau_str_gpe)*gsyn_gaba_str_gpe : 1

I_chem_GPe_GPe = G_gpe_gpe*gsyn_gaba_gpe_gpe*(E_gpe_gpe - v) : amp
dgsyn_gaba_gpe_gpe/dt = -(1/tau_gpe_gpe)*gsyn_gaba_gpe_gpe : 1

I_chem_STN_GPe = G_stn_gpe*gsyn_ampa_stn_gpe*(E_stn_gpe - v) + B*G_stn_gpe*0.36*gsyn_nmda_stn_gpe*(E_stn_gpe - v) : amp
dgsyn_ampa_stn_gpe/dt = -(1/tau_stn_gpe_ampa)*gsyn_ampa_stn_gpe : 1 
dgsyn_nmda_stn_gpe/dt = -(1/tau_stn_gpe_nmda)*gsyn_nmda_stn_gpe : 1
'''