from brian2 import *
from parameters import *
from equations import *

""" All the populations' NeuronGroup, first the STN ones and then the GPe ones and finally
    the Cortical Poisson Group
"""
N_STN = N_STN_RB + N_STN_LLRS + N_STN_NR
STNGroup = NeuronGroup(N_STN, eqs_STN, threshold='v>v_peak_STN+U*u2*ms', 
reset='v=cSTN-U*u2*ms;u1=u1+dSTN1;u2=u2+dSTN2', method='euler')

STNRBGroup = STNGroup[:27]
STNLLRSGroup = STNGroup[27:38]
STNNRGroup = STNGroup[38:]

STNRBGroup.CSTN = CSTN_RB
STNRBGroup.v_peak_STN = v_peak_STN_RB
STNRBGroup.v_thres_STN = v_thres_STN_RB
STNRBGroup.v_rest_STN1 = v_rest_STN1_RB
STNRBGroup.v_rest_STN2 = v_rest_STN2_RB
STNRBGroup.kSTN = kSTN_RB
STNRBGroup.aSTN1 = aSTN1_RB
STNRBGroup.aSTN2 = aSTN2_RB
STNRBGroup.bSTN1 = bSTN1_RB
STNRBGroup.bSTN2 = bSTN2_RB
STNRBGroup.cSTN = cSTN_RB
STNRBGroup.dSTN1 = dSTN1_RB
STNRBGroup.dSTN2 = dSTN2_RB
STNRBGroup.w1 = w1_RB
STNRBGroup.w2 = w2_RB
STNRBGroup.ISTN_ext = ISTN_ext_RB


STNLLRSGroup.CSTN = CSTN_LLRS
STNLLRSGroup.v_peak_STN = v_peak_STN_LLRS
STNLLRSGroup.v_thres_STN = v_thres_STN_LLRS
STNLLRSGroup.v_rest_STN1 = v_rest_STN1_LLRS
STNLLRSGroup.v_rest_STN2 = v_rest_STN2_LLRS
STNLLRSGroup.kSTN = kSTN_LLRS
STNLLRSGroup.aSTN1 = aSTN1_LLRS
STNLLRSGroup.aSTN2 = aSTN2_LLRS
STNLLRSGroup.bSTN1 = bSTN1_LLRS
STNLLRSGroup.bSTN2 = bSTN2_LLRS
STNLLRSGroup.cSTN = cSTN_LLRS
STNLLRSGroup.dSTN1 = dSTN1_LLRS
STNLLRSGroup.dSTN2 = dSTN2_LLRS
STNLLRSGroup.w1 = w1_LLRS
STNLLRSGroup.w2 = w2_LLRS
STNLLRSGroup.ISTN_ext = ISTN_ext_LLRS

STNNRGroup.CSTN = CSTN_NR
STNNRGroup.v_peak_STN = v_peak_STN_NR
STNNRGroup.v_thres_STN = v_thres_STN_NR
STNNRGroup.v_rest_STN1 = v_rest_STN1_NR
STNNRGroup.v_rest_STN2 = v_rest_STN2_NR
STNNRGroup.kSTN = kSTN_NR
STNNRGroup.aSTN1 = aSTN1_NR
STNNRGroup.aSTN2 = aSTN2_NR
STNNRGroup.bSTN1 = bSTN1_NR
STNNRGroup.bSTN2 = bSTN2_NR
STNNRGroup.cSTN = cSTN_NR
STNNRGroup.dSTN1 = dSTN1_NR
STNNRGroup.dSTN2 = dSTN2_NR
STNNRGroup.w1 = w1_NR
STNNRGroup.w2 = w2_NR
STNNRGroup.ISTN_ext = ISTN_ext_NR

N_GPe = N_GPe_A + N_GPe_B + N_GPe_C
GPeGroup = NeuronGroup(N_GPe, eqs_GPe, threshold='v>v_peak_GPe', reset='v=cGPe;u=u+dGPe', method='euler')
#GPeGroup = PoissonGroup(N_GPe, rates=30*Hz)

GPeAGroup = GPeGroup[:6]
GPeBGroup = GPeGroup[6:136]
GPeCGroup = GPeGroup[136:]

GPeAGroup.CGPe = CGPe_A
GPeAGroup.v_thres_GPe = v_thres_GPe_A
GPeAGroup.v_peak_GPe = v_peak_GPe_A
GPeAGroup.v_rest_GPe = v_rest_GPe_A
GPeAGroup.kGPe = kGPe_A
GPeAGroup.aGPe = aGPe_A
GPeAGroup.bGPe = bGPe_A
GPeAGroup.cGPe = cGPe_A
GPeAGroup.dGPe = dGPe_A
GPeAGroup.IGPe_ext = IGPe_ext_A
GPeAGroup.sigma_GPe = sigma_GPe_A

GPeBGroup.CGPe = CGPe_B
GPeBGroup.v_thres_GPe = v_thres_GPe_B
GPeBGroup.v_peak_GPe = v_peak_GPe_B
GPeBGroup.v_rest_GPe = v_rest_GPe_B
GPeBGroup.kGPe = kGPe_B
GPeBGroup.aGPe = aGPe_B
GPeBGroup.bGPe = bGPe_B
GPeBGroup.cGPe = cGPe_B
GPeBGroup.dGPe = dGPe_B
GPeBGroup.IGPe_ext = IGPe_ext_B
GPeBGroup.sigma_GPe = sigma_GPe_B

GPeCGroup.CGPe = CGPe_C
GPeCGroup.v_thres_GPe = v_thres_GPe_C
GPeCGroup.v_peak_GPe = v_peak_GPe_C
GPeCGroup.v_rest_GPe = v_rest_GPe_C
GPeCGroup.kGPe = kGPe_C
GPeCGroup.aGPe = aGPe_C
GPeCGroup.bGPe = bGPe_C
GPeCGroup.cGPe = cGPe_C
GPeCGroup.dGPe = dGPe_C
GPeCGroup.IGPe_ext = IGPe_ext_C
GPeCGroup.sigma_GPe = sigma_GPe_C

CorticalGroup = PoissonGroup(N_input_CTX, rates=rate_CTX)
StriatalGroup = PoissonGroup(N_input_MSN2, rates=rate_STR)

""" Striatum to GPe synapse
"""
ChemicalSTRGPe = Synapses(StriatalGroup, GPeGroup, delay=lambda_str_gpe,
on_pre="gsyn_gaba_str_gpe+=gstrgpe")
ChemicalSTRGPe.connect(True, p=p_STR_GPe)

""" Cortex to STN synapse
"""
ChemicalCTXSTN = Synapses(CorticalGroup, STNGroup, delay=lambda_ctx_stn, 
on_pre="gsyn_ampa_ctx_stn+=gctxstn;gsyn_nmda_ctx_stn+=gctxstn")
ChemicalCTXSTN.connect(True, p=p_CTX_STN)

""" GPe to GPe synapses
"""
ChemicalGPeGPe = Synapses(GPeGroup, GPeGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=ggpegpe")
ChemicalGPeGPe.connect(True, p=p_GPe_GPe)

""" GPe to STN synapses
"""
ChemicalGPeSTN = Synapses(GPeGroup, STNGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=ggpestn")
ChemicalGPeSTN.connect(True, p=p_GPe_STN)

""" STN to GPe synapses
"""
ChemicalSTNGPe = Synapses(STNGroup, GPeGroup,delay=lambda_stn_gpe, model='w:volt',
on_pre="gsyn_ampa_stn_gpe+=gstngpe;gsyn_nmda_stn_gpe+=gstngpe")
ChemicalSTNGPe.connect(True, p=p_STN_GPe)