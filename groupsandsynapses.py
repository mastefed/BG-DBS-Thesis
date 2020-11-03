from brian2 import *
from parameters import *
from equations import *



""" All the populations' NeuronGroup, first the STN ones and then the GPe ones and finally
    the Cortical Poisson Group
"""
STNRBGroup = NeuronGroup(N_STN_RB, eqs_STN_RB, threshold='v>v_peak_STN_RB+U*u2*ms', 
reset='v=cSTN_RB-U*u2*ms;u1=u1+dSTN1_RB;u2=u2+dSTN2_RB', method='euler')

STNLLRSGroup = NeuronGroup(N_STN_LLRS, eqs_STN_LLRS, threshold='v>v_peak_STN_LLRS+U*u2*ms', 
reset='v=cSTN_LLRS-U*u2*ms;u1=u1+dSTN1_LLRS;u2=u2+dSTN2_LLRS', method='euler')

STNNRGroup = NeuronGroup(N_STN_NR, eqs_STN_NR, threshold='v>v_peak_STN_NR+U*u2*ms', 
reset='v=cSTN_NR-U*u2*ms;u1=u1+dSTN1_NR;u2=u2+dSTN2_NR', method='euler')

GPeAGroup = NeuronGroup(N_GPe_A, eqs_GPe_A, threshold='v>v_peak_GPe_A', reset='v=cGPe_A;u=u+dGPe_A', method='euler')

GPeBGroup = NeuronGroup(N_GPe_B, eqs_GPe_B, threshold='v>v_peak_GPe_B', reset='v=cGPe_B;u=u+dGPe_B', method='euler')

GPeCGroup = NeuronGroup(N_GPe_C, eqs_GPe_C, threshold='v>v_peak_GPe_C', reset='v=cGPe_C;u=u+dGPe_C', method='euler')

CorticalGroup = PoissonGroup(N_input, rates='input_rates(t)')

# g is the synapses' efficacy
g = 0.001

""" Cortex to STN synapse
"""
ChemicalCTXSTNRB = Synapses(CorticalGroup, STNRBGroup, delay=lambda_ctx_stn, 
on_pre="gsyn_ampa_ctx_stn+=g;gsyn_nmda_ctx_stn+=g")
ChemicalCTXSTNRB.connect(True, p=p_CTX_STN)

ChemicalCTXSTNLLRS = Synapses(CorticalGroup, STNLLRSGroup, delay=lambda_ctx_stn, 
on_pre="gsyn_ampa_ctx_stn+=g;gsyn_nmda_ctx_stn+=g")
ChemicalCTXSTNLLRS.connect(True, p=p_CTX_STN)

ChemicalCTXSTNNR = Synapses(CorticalGroup, STNNRGroup, delay=lambda_ctx_stn, 
on_pre="gsyn_ampa_ctx_stn+=g;gsyn_nmda_ctx_stn+=g")
ChemicalCTXSTNNR.connect(True, p=p_CTX_STN)


""" GPe to GPe synapses
"""
# Self connections
ChemicalGPeAGPeA = Synapses(GPeAGroup, GPeAGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeAGPeA.connect(True, p=p_GPe_GPe)

ChemicalGPeBGPeB = Synapses(GPeBGroup, GPeBGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeBGPeB.connect(True, p=p_GPe_GPe)

ChemicalGPeCGPeC = Synapses(GPeCGroup, GPeCGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeCGPeC.connect(True, p=p_GPe_GPe)

# A to others
ChemicalGPeAGPeB = Synapses(GPeAGroup, GPeBGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeAGPeB.connect(True, p=p_GPe_GPe)

ChemicalGPeAGPeC = Synapses(GPeAGroup, GPeCGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeAGPeC.connect(True, p=p_GPe_GPe)

# B to others
ChemicalGPeBGPeC = Synapses(GPeBGroup, GPeCGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeBGPeC.connect(True, p=p_GPe_GPe)

ChemicalGPeBGPeA = Synapses(GPeBGroup, GPeAGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeBGPeA.connect(True, p=p_GPe_GPe)

# C to others
ChemicalGPeCGPeA = Synapses(GPeCGroup, GPeAGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeCGPeA.connect(True, p=p_GPe_GPe)

ChemicalGPeCGPeB = Synapses(GPeCGroup, GPeBGroup, delay=lambda_gpe_gpe, model='w:volt', on_pre="gsyn_gaba_gpe_gpe+=g")
ChemicalGPeCGPeB.connect(True, p=p_GPe_GPe)


""" GPe to STN synapses
"""
# A to RB/LLRS/NR
ChemicalGPeASTNRB = Synapses(GPeAGroup, STNRBGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeASTNRB.connect(True, p=p_GPe_STN)

ChemicalGPeASTNLLRS = Synapses(GPeAGroup, STNLLRSGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeASTNLLRS.connect(True, p=p_GPe_STN)

ChemicalGPeASTNNR = Synapses(GPeAGroup, STNNRGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeASTNNR.connect(True, p=p_GPe_STN)

# B to RB/LLRS/NR
ChemicalGPeBSTNRB = Synapses(GPeBGroup, STNRBGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeBSTNRB.connect(True, p=p_GPe_STN)

ChemicalGPeBSTNLLRS = Synapses(GPeBGroup, STNLLRSGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeBSTNLLRS.connect(True, p=p_GPe_STN)

ChemicalGPeBSTNNR = Synapses(GPeBGroup, STNNRGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeBSTNNR.connect(True, p=p_GPe_STN)

# C to RB/LLRS/NR
ChemicalGPeCSTNRB = Synapses(GPeCGroup, STNRBGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeCSTNRB.connect(True, p=p_GPe_STN)

ChemicalGPeCSTNLLRS = Synapses(GPeCGroup, STNLLRSGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeCSTNLLRS.connect(True, p=p_GPe_STN)

ChemicalGPeCSTNNR = Synapses(GPeCGroup, STNNRGroup, delay=lambda_gpe_stn, model='w:volt', on_pre="gsyn_gaba_gpe_stn+=g")
ChemicalGPeCSTNNR.connect(True, p=p_GPe_STN)


""" STN to GPe synapses
"""
# RB to A/B/C
ChemicalSTNRBGPeA = Synapses(STNRBGroup, GPeAGroup,delay=lambda_stn_gpe, model='w:volt',
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNRBGPeA.connect(True, p=p_STN_GPe)

ChemicalSTNRBGPeB = Synapses(STNRBGroup, GPeBGroup,delay=lambda_stn_gpe, model='w:volt',  
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNRBGPeB.connect(True, p=p_STN_GPe)

ChemicalSTNRBGPeC = Synapses(STNRBGroup, GPeCGroup,delay=lambda_stn_gpe, model='w:volt', 
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNRBGPeC.connect(True, p=p_STN_GPe)

# LLRS to A/B/C
ChemicalSTNLLRSGPeA = Synapses(STNLLRSGroup, GPeAGroup,delay=lambda_stn_gpe, model='w:volt', 
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNLLRSGPeA.connect(True, p=p_STN_GPe)

ChemicalSTNLLRSGPeB = Synapses(STNLLRSGroup, GPeBGroup,delay=lambda_stn_gpe, model='w:volt', 
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNLLRSGPeB.connect(True, p=p_STN_GPe)

ChemicalSTNLLRSGPeC = Synapses(STNLLRSGroup, GPeCGroup,delay=lambda_stn_gpe, model='w:volt', 
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNLLRSGPeC.connect(True, p=p_STN_GPe)

# NR to A/B/C
ChemicalSTNNRGPeA = Synapses(STNNRGroup, GPeAGroup,delay=lambda_stn_gpe, model='w:volt', 
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNNRGPeA.connect(True, p=p_STN_GPe)

ChemicalSTNNRGPeB = Synapses(STNNRGroup, GPeBGroup,delay=lambda_stn_gpe, model='w:volt', 
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNNRGPeB.connect(True, p=p_STN_GPe)

ChemicalSTNNRGPeC = Synapses(STNNRGroup, GPeCGroup,delay=lambda_stn_gpe, model='w:volt', 
on_pre="gsyn_ampa_stn_gpe+=g;gsyn_nmda_stn_gpe+=g")
ChemicalSTNNRGPeC.connect(True, p=p_STN_GPe)
