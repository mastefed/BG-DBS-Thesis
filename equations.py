""" Equations for NeuronGroups and Synapses
"""
import brian2 as b2

""" Heaviside function
"""
H = b2.core.functions.DEFAULT_FUNCTIONS['int']
adimvolt = 1/b2.mV # I need this to make v_rest_STN2 - v adimensional, else Dimension Mismatch error will pop up.


""" RB, LLRS and NR populations of STN
"""
eqs_STN_RB = '''
dv/dt = (1/CSTN_RB)*(kSTN_RB*(v - v_rest_STN1_RB)*(v - v_thres_STN_RB) - u1 - w2_RB*u2 + I_tot + sigma*CSTN_RB*xi) : volt
du1/dt = aSTN1_RB*(bSTN1_RB*(v - v_rest_STN1_RB) - u1) : volt/ohm
du2/dt = aSTN2_RB*(bSTN2_RB*H( adimvolt*(v_rest_STN2_RB - v) >= 0)*(v - v_rest_STN2_RB) - u2) : volt

U = 1/(w1_RB*abs(u2)+w3_RB) : 1

I_tot = I_syn_tot + ISTN_ext_RB : amp

I_syn_tot = I_chem_CTX_STN + I_chem_GPe_STN : amp

I_chem_CTX_STN = G_ctx_stn*gsyn_ampa_ctx_stn*(E_ctx_stn - v) + G_ctx_stn*0.6*gsyn_nmda_ctx_stn*(E_ctx_stn - v) : amp
dgsyn_ampa_ctx_stn/dt = -(1/tau_ctx_stn_ampa)*gsyn_ampa_ctx_stn : 1
dgsyn_nmda_ctx_stn/dt = -(1/tau_ctx_stn_nmda)*gsyn_nmda_ctx_stn : 1

I_chem_GPe_STN = G_gpe_stn*gsyn_gaba_gpe_stn*(E_gpe_stn - v) : amp
dgsyn_gaba_gpe_stn/dt = -(1/tau_gpe_stn)*gsyn_gaba_gpe_stn : 1
'''

eqs_STN_LLRS = '''
dv/dt = (1/CSTN_LLRS)*(kSTN_LLRS*(v - v_rest_STN1_LLRS)*(v - v_thres_STN_LLRS) - u1 - w2_LLRS*u2 + I_tot + sigma*CSTN_LLRS*xi) : volt
du1/dt = aSTN1_LLRS*(bSTN1_LLRS*(v - v_rest_STN1_LLRS) - u1) : volt/ohm
du2/dt = aSTN2_LLRS*(bSTN2_LLRS*H( adimvolt*(v_rest_STN2_LLRS - v) >= 0)*(v - v_rest_STN2_LLRS) - u2) : volt

U = 1/(w1_LLRS*abs(u2)+w3_LLRS) : 1

I_tot = I_syn_tot + ISTN_ext_LLRS : amp

I_syn_tot = I_chem_CTX_STN + I_chem_GPe_STN : amp

I_chem_CTX_STN = G_ctx_stn*gsyn_ampa_ctx_stn*(E_ctx_stn - v) + G_ctx_stn*0.6*gsyn_nmda_ctx_stn*(E_ctx_stn - v) : amp
dgsyn_ampa_ctx_stn/dt = -(1/tau_ctx_stn_ampa)*gsyn_ampa_ctx_stn : 1
dgsyn_nmda_ctx_stn/dt = -(1/tau_ctx_stn_nmda)*gsyn_nmda_ctx_stn : 1

I_chem_GPe_STN = G_gpe_stn*gsyn_gaba_gpe_stn*(E_gpe_stn - v) : amp
dgsyn_gaba_gpe_stn/dt = -(1/tau_gpe_stn)*gsyn_gaba_gpe_stn : 1
'''

eqs_STN_NR = '''
dv/dt = (1/CSTN_NR)*(kSTN_NR*(v - v_rest_STN1_NR)*(v - v_thres_STN_NR) - u1 - w2_NR*u2 + I_tot + sigma*CSTN_NR*xi) : volt
du1/dt = aSTN1_NR*(bSTN1_NR*(v - v_rest_STN1_NR) - u1) : volt/ohm
du2/dt = aSTN2_NR*(bSTN2_NR*H( adimvolt*(v_rest_STN2_NR - v) >= 0)*(v - v_rest_STN2_NR) - u2) : volt

U = 1/(w1_NR*abs(u2)+w3_NR) : 1

I_tot = I_syn_tot + ISTN_ext_NR : amp

I_syn_tot = I_chem_CTX_STN + I_chem_GPe_STN : amp

I_chem_CTX_STN = G_ctx_stn*gsyn_ampa_ctx_stn*(E_ctx_stn - v) + G_ctx_stn*0.6*gsyn_nmda_ctx_stn*(E_ctx_stn - v) : amp
dgsyn_ampa_ctx_stn/dt = -(1/tau_ctx_stn_ampa)*gsyn_ampa_ctx_stn : 1
dgsyn_nmda_ctx_stn/dt = -(1/tau_ctx_stn_nmda)*gsyn_nmda_ctx_stn : 1

I_chem_GPe_STN = G_gpe_stn*gsyn_gaba_gpe_stn*(E_gpe_stn - v) : amp
dgsyn_gaba_gpe_stn/dt = -(1/tau_gpe_stn)*gsyn_gaba_gpe_stn : 1
'''

""" A,B and C populations of GPe
"""
eqs_GPe_A = '''
dv/dt = (1/CGPe_A)*(kGPe_A*(v - v_rest_GPe_A)*(v - v_thres_GPe_A) - u + I_tot + sigma*CGPe_A*xi) : volt
du/dt = aGPe_A*(bGPe_A*(v - v_rest_GPe_A) - u) : volt/ohm

I_tot = I_syn_tot + IGPe_ext_A : amp

I_syn_tot = I_chem_GPe_GPe + I_chem_STN_GPe : amp

I_chem_GPe_GPe = G_gpe_gpe*gsyn_gaba_gpe_gpe*(E_gpe_gpe - v) : amp
dgsyn_gaba_gpe_gpe/dt = -(1/tau_gpe_gpe)*gsyn_gaba_gpe_gpe : 1

I_chem_STN_GPe = G_stn_gpe*gsyn_ampa_stn_gpe*(E_stn_gpe - v) + G_stn_gpe*0.36*gsyn_nmda_stn_gpe*(E_stn_gpe - v) : amp
dgsyn_ampa_stn_gpe/dt = -(1/tau_stn_gpe_ampa)*gsyn_ampa_stn_gpe : 1 
dgsyn_nmda_stn_gpe/dt = -(1/tau_stn_gpe_nmda)*gsyn_nmda_stn_gpe : 1
'''

eqs_GPe_B = '''
dv/dt = (1/CGPe_B)*(kGPe_B*(v - v_rest_GPe_B)*(v - v_thres_GPe_B) - u + I_tot + sigma*CGPe_B*xi) : volt
du/dt = aGPe_B*(bGPe_B*(v - v_rest_GPe_B) - u) : volt/ohm

I_tot = I_syn_tot + IGPe_ext_B : amp

I_syn_tot = I_chem_GPe_GPe + I_chem_STN_GPe : amp

I_chem_GPe_GPe = G_gpe_gpe*gsyn_gaba_gpe_gpe*(E_gpe_gpe - v) : amp
dgsyn_gaba_gpe_gpe/dt = -(1/tau_gpe_gpe)*gsyn_gaba_gpe_gpe : 1

I_chem_STN_GPe = G_stn_gpe*gsyn_ampa_stn_gpe*(E_stn_gpe - v) + G_stn_gpe*0.36*gsyn_nmda_stn_gpe*(E_stn_gpe - v) : amp
dgsyn_ampa_stn_gpe/dt = -(1/tau_stn_gpe_ampa)*gsyn_ampa_stn_gpe : 1 
dgsyn_nmda_stn_gpe/dt = -(1/tau_stn_gpe_nmda)*gsyn_nmda_stn_gpe : 1
'''

eqs_GPe_C = '''
dv/dt = (1/CGPe_C)*(kGPe_C*(v - v_rest_GPe_C)*(v - v_thres_GPe_C) - u + I_tot + sigma*CGPe_C*xi) : volt
du/dt = aGPe_C*(bGPe_C*(v - v_rest_GPe_C) - u) : volt/ohm

I_tot = I_syn_tot + IGPe_ext_C : amp

I_syn_tot = I_chem_GPe_GPe + I_chem_STN_GPe : amp

I_chem_GPe_GPe = G_gpe_gpe*gsyn_gaba_gpe_gpe*(E_gpe_gpe - v) : amp
dgsyn_gaba_gpe_gpe/dt = -(1/tau_gpe_gpe)*gsyn_gaba_gpe_gpe : 1

I_chem_STN_GPe = G_stn_gpe*gsyn_ampa_stn_gpe*(E_stn_gpe - v) + G_stn_gpe*0.36*gsyn_nmda_stn_gpe*(E_stn_gpe - v) : amp
dgsyn_ampa_stn_gpe/dt = -(1/tau_stn_gpe_ampa)*gsyn_ampa_stn_gpe : 1 
dgsyn_nmda_stn_gpe/dt = -(1/tau_stn_gpe_nmda)*gsyn_nmda_stn_gpe : 1
'''
