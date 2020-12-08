""" Code to retrieve single neuron
    characteristics
"""
from brian2 import *
import random as ran
import numpy as np
import builtins

N_GPe_pap = 153 # In realtà 152
N_GPe_B = int(N_GPe_pap * 0.85)
N_GPe_A = int(N_GPe_pap * 0.0405)
N_GPe_C = int(N_GPe_pap * 0.1095)
    
N_STN_pap = 45 # In realtà 44
N_STN_RB = int(N_STN_pap * 0.6)
N_STN_LLRS = int(N_STN_pap * 0.25)
N_STN_NR = int(N_STN_pap * 0.15)

deft = defaultclock.dt

""" STN RB Neurons 
"""
CSTN_RB = 23.*pfarad
v_peak_STN_RB = 15.4*mV
v_thres_STN_RB = -41.4*mV
v_rest_STN1_RB = -56.2*mV
v_rest_STN2_RB = -60.*mV
b_tresh_STN_RB = v_rest_STN2_RB
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

# ISTN_ext_RB = 56.1*pamp
ISTN_ext_RB = 0.*pamp

sigma_stn = 0.5

""" STN LLRS Neurons 
"""
CSTN_LLRS = 40.*pfarad
v_peak_STN_LLRS = 15.4*mV
v_thres_STN_LLRS = -50.*mV
v_rest_STN1_LLRS = -56.2*mV
v_rest_STN2_LLRS = -60.*mV
b_tresh_STN_LLRS = v_rest_STN2_LLRS
kSTN_LLRS = 0.3 
aSTN1_LLRS = 0.05/ms
aSTN2_LLRS = 0.001/ms # 0.001
bSTN1_LLRS = 0.2/ms # 0.2
bSTN2_LLRS = 0.3/ms
cSTN_LLRS = -60.*mV
dSTN1_LLRS = 1000*mV/ms
dSTN2_LLRS = 10*mV/ms # 10
w1_LLRS = 0.01
w2_LLRS = 0.

# ISTN_ext_LLRS = 8.*pamp
ISTN_ext_LLRS = 0.*pamp

sigma_stn = 0.5

# ISTN_ext_LLRS = 8.*pamp
ISTN_ext_LLRS = 0.*pamp

sigma_stn = 0.5

""" STN NR Neurons 
"""
CSTN_NR = 30.*pfarad
v_peak_STN_NR = 15.4*mV
v_thres_STN_NR = -43.75*mV
v_rest_STN1_NR = -58.5*mV
v_rest_STN2_NR = -43.2*mV
b_tresh_STN_NR = 5000.*mV # This value is incredibly high just to make the Heaviside in STN NR be always set to 1 
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

# ISTN_ext_NR = -18.*pamp
ISTN_ext_NR = 0.*pamp

sigma_stn = 0.5

######################################################## GPe
""" GPe A
"""
CGPe_A = 70.*pfarad
v_thres_GPe_A = -42.*mV
v_peak_GPe_A = 38.*mV
v_rest_GPe_A = -50.7*mV
kGPe_A = 0.06 
aGPe_A = 0.29*(1/ms)
bGPe_A = 4.26*(1/ms)
cGPe_A = -57.4*mV
dGPe_A = 110*mV/ms
IGPe_ext_A = 167*pamp
sigma_GPe_A = 3 #0.7

""" GPe B
"""
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
sigma_GPe_B = 3 #1.6

""" GPe C
"""
CGPe_C = 65.*pfarad
v_thres_GPe_C = -43.*mV
v_peak_GPe_C = 34.5*mV
v_rest_GPe_C = -54.*mV
kGPe_C = 0.099
aGPe_C = 0.42*(1/ms)
bGPe_C = 7*(1/ms)
cGPe_C = -52.*mV
dGPe_C = 166*mV/ms
IGPe_ext_C = 237.5*pamp
sigma_GPe_C = 3 #1.3


def normalstate():
    eqs_STN = '''
    dv/dt = (1/CSTN)*(kSTN*(v - v_rest_STN1)*(v - v_thres_STN)*nS/mV - u1*pF - w2*u2*pF + I_tot) + sigma_stn*xi*mV/ms**.5 : volt
    du1/dt = aSTN1*(bSTN1*(v - v_rest_STN1) - u1) : volt/second
    du2/dt = aSTN2*(bSTN2*H*(v - v_rest_STN2) - u2) : volt/second

    U = 1/(w1*abs(u2)*second/volt + 1/w1) : 1

    H = int(b_thresh >= v) : 1 

    CSTN : farad
    v_peak_STN : volt
    v_thres_STN : volt
    v_rest_STN1 : volt
    v_rest_STN2 : volt
    b_thresh : volt
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

    I_tot = I_pulse(t) + ISTN_ext : amp
    '''

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

    I_tot = I_pulse(t) + IGPe_ext : amp
    '''

    N_STN = N_STN_RB + N_STN_LLRS + N_STN_NR
    N_GPe = N_GPe_A + N_GPe_B + N_GPe_C

    STNGroup = NeuronGroup(N_STN, eqs_STN, threshold='v>v_peak_STN+U*u2*ms', reset='v=cSTN-U*u2*ms;u1=u1+dSTN1;u2=u2+dSTN2', method='euler')
    GPeGroup = NeuronGroup(N_GPe, eqs_GPe, threshold='v>v_peak_GPe', reset='v=cGPe;u=u+dGPe', method='euler')
    
    return STNGroup, GPeGroup

def nou1():
    eqs_STN = '''
    dv/dt = (1/CSTN)*(kSTN*(v - v_rest_STN1)*(v - v_thres_STN)*nS/mV - u1*pF + I_tot) + sigma_stn*xi*mV/ms**.5 : volt
    du1/dt = aSTN1*(bSTN1*(v - v_rest_STN1) - u1) : volt/second

    CSTN : farad
    v_peak_STN : volt
    v_thres_STN : volt
    v_rest_STN1 : volt
    v_rest_STN2 : volt
    b_thresh : volt
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

    I_tot = I_pulse(t) + ISTN_ext : amp
    '''
    
    eqs_GPe = '''
    dv/dt = (1/CGPe)*(kGPe*pF/ms/mV*(v - v_rest_GPe)*(v - v_thres_GPe) + I_tot) + sigma_GPe*xi*mV/ms**.5 : volt

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

    I_tot = I_pulse(t) + IGPe_ext : amp
    '''

    N_STN = N_STN_RB + N_STN_LLRS + N_STN_NR
    N_GPe = N_GPe_A + N_GPe_B + N_GPe_C

    STNGroup = NeuronGroup(N_STN, eqs_STN, threshold='v>v_peak_STN', reset='v=cSTN;u1=u1+dSTN1', method='euler')
    GPeGroup = NeuronGroup(N_GPe, eqs_GPe, threshold='v>v_peak_GPe', reset='v=cGPe', method='euler')

    return STNGroup, GPeGroup

def nouboth():
    eqs_STN = '''
    dv/dt = (1/CSTN)*(kSTN*(v - v_rest_STN1)*(v - v_thres_STN)*nS/mV + I_tot) + sigma_stn*xi*mV/ms**.5 : volt

    CSTN : farad
    v_peak_STN : volt
    v_thres_STN : volt
    v_rest_STN1 : volt
    v_rest_STN2 : volt
    b_thresh : volt
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

    I_tot = I_pulse(t) + ISTN_ext : amp
    '''
    
    eqs_GPe = '''
    dv/dt = (1/CGPe)*(kGPe*pF/ms/mV*(v - v_rest_GPe)*(v - v_thres_GPe) + I_tot) + sigma_GPe*xi*mV/ms**.5 : volt

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

    I_tot = I_pulse(t) + IGPe_ext : amp
    '''

    N_STN = N_STN_RB + N_STN_LLRS + N_STN_NR
    N_GPe = N_GPe_A + N_GPe_B + N_GPe_C

    STNGroup = NeuronGroup(N_STN, eqs_STN, threshold='v>v_peak_STN', reset='v=cSTN', method='euler')
    GPeGroup = NeuronGroup(N_GPe, eqs_GPe, threshold='v>v_peak_GPe', reset='v=cGPe', method='euler')

    return STNGroup, GPeGroup

STNGroup, GPeGroup = normalstate()
#STNGroup, GPeGroup = nou1()
#STNGroup, GPeGroup = nouboth()

STNRBGroup = STNGroup[:27]
STNLLRSGroup = STNGroup[27:38]
STNNRGroup = STNGroup[38:]

STNRBGroup.v = v_rest_STN1_RB
STNRBGroup.CSTN = CSTN_RB
STNRBGroup.v_peak_STN = v_peak_STN_RB
STNRBGroup.v_thres_STN = v_thres_STN_RB
STNRBGroup.v_rest_STN1 = v_rest_STN1_RB
STNRBGroup.v_rest_STN2 = v_rest_STN2_RB
STNRBGroup.b_thresh = b_tresh_STN_RB
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

STNLLRSGroup.v = v_rest_STN1_LLRS
STNLLRSGroup.CSTN = CSTN_LLRS
STNLLRSGroup.v_peak_STN = v_peak_STN_LLRS
STNLLRSGroup.v_thres_STN = v_thres_STN_LLRS
STNLLRSGroup.v_rest_STN1 = v_rest_STN1_LLRS
STNLLRSGroup.v_rest_STN2 = v_rest_STN2_LLRS
STNLLRSGroup.b_thresh = b_tresh_STN_LLRS
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

STNNRGroup.v = v_rest_STN1_NR
STNNRGroup.CSTN = CSTN_NR
STNNRGroup.v_peak_STN = v_peak_STN_NR
STNNRGroup.v_thres_STN = v_thres_STN_NR
STNNRGroup.v_rest_STN1 = v_rest_STN1_NR
STNNRGroup.v_rest_STN2 = v_rest_STN2_NR
STNNRGroup.b_thresh = b_tresh_STN_NR
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

GPeAGroup = GPeGroup[:6]
GPeBGroup = GPeGroup[6:136]
GPeCGroup = GPeGroup[136:]

GPeAGroup.v = v_rest_GPe_A
GPeAGroup.CGPe = CGPe_A
GPeAGroup.v_thres_GPe = v_thres_GPe_A
GPeAGroup.v_peak_GPe = v_peak_GPe_A
GPeAGroup.v_rest_GPe = v_rest_GPe_A
GPeAGroup.kGPe = kGPe_A
GPeAGroup.aGPe = aGPe_A
GPeAGroup.bGPe = bGPe_A
GPeAGroup.cGPe = cGPe_A
GPeAGroup.dGPe = dGPe_A
GPeAGroup.sigma_GPe = sigma_GPe_A

#GPeAGroup.IGPe_ext = 0.*pamp 
GPeAGroup.IGPe_ext = IGPe_ext_A

GPeBGroup.v = v_rest_GPe_B
GPeBGroup.CGPe = CGPe_B
GPeBGroup.v_thres_GPe = v_thres_GPe_B
GPeBGroup.v_peak_GPe = v_peak_GPe_B
GPeBGroup.v_rest_GPe = v_rest_GPe_B
GPeBGroup.kGPe = kGPe_B
GPeBGroup.aGPe = aGPe_B
GPeBGroup.bGPe = bGPe_B
GPeBGroup.cGPe = cGPe_B
GPeBGroup.dGPe = dGPe_B
GPeBGroup.sigma_GPe = sigma_GPe_B

#GPeBGroup.IGPe_ext = 0.*pamp 
GPeBGroup.IGPe_ext = IGPe_ext_B

GPeCGroup.v = v_rest_GPe_C
GPeCGroup.CGPe = CGPe_C
GPeCGroup.v_thres_GPe = v_thres_GPe_C
GPeCGroup.v_peak_GPe = v_peak_GPe_C
GPeCGroup.v_rest_GPe = v_rest_GPe_C
GPeCGroup.kGPe = kGPe_C
GPeCGroup.aGPe = aGPe_C
GPeCGroup.bGPe = bGPe_C
GPeCGroup.cGPe = cGPe_C
GPeCGroup.dGPe = dGPe_C
GPeCGroup.sigma_GPe = sigma_GPe_C

#GPeCGroup.IGPe_ext = 0.*pamp
GPeCGroup.IGPe_ext = IGPe_ext_C


spikemonitorSTN = SpikeMonitor(STNGroup, variables=['v'])
statemonitorSTN = StateMonitor(STNGroup, ['v'], record=True)

statemonitorSTNRB = StateMonitor(STNRBGroup, ['v'], record=True)
spikemonitorSTNRB = SpikeMonitor(STNRBGroup, variables=['v'])

statemonitorSTNLLRS = StateMonitor(STNLLRSGroup, ['v'], record=True)
spikemonitorSTNLLRS = SpikeMonitor(STNLLRSGroup, variables=['v'])

statemonitorSTNNR = StateMonitor(STNNRGroup, ['v'], record=True)
spikemonitorSTNNR = SpikeMonitor(STNNRGroup, variables=['v'])

spikemonitorGPe = SpikeMonitor(GPeGroup, variables=['v'])
statemonitorGPe = StateMonitor(GPeGroup, ['v'], record=True)
    
statemonitorGPeA = StateMonitor(GPeAGroup, variables=['v'], record=True)
spikemonitorGPeA = SpikeMonitor(GPeAGroup, variables=['v'])
    
statemonitorGPeB = StateMonitor(GPeBGroup, variables=['v'], record=True)
spikemonitorGPeB = SpikeMonitor(GPeBGroup, variables=['v'])
    
statemonitorGPeC = StateMonitor(GPeCGroup, variables=['v'], record=True)
spikemonitorGPeC = SpikeMonitor(GPeCGroup, variables=['v'])

store()

def frrates():
    frstnrb = []
    frstnllrs = []
    frstnnr = []
    frgpea = []
    frgpeb = []
    frgpec = []

    k = 1

    for I in np.arange(-300.,0.,20.):
        restore()
        I_pulse = TimedArray(
            [I, 0, 0, 0, 0]*pamp,
            dt=200*ms
        )
        run(sim_time)
        frstnrb.append(np.mean(spikemonitorSTNRB.count/sim_time))
        frstnllrs.append(np.mean(spikemonitorSTNLLRS.count/sim_time))
        frstnnr.append(np.mean(spikemonitorSTNNR.count/sim_time))
        frgpea.append(np.mean(spikemonitorGPeA.count/sim_time))
        frgpeb.append(np.mean(spikemonitorGPeB.count/sim_time))
        frgpec.append(np.mean(spikemonitorGPeC.count/sim_time))
        print(f"Processo {k} completato!\n")
        k += 1

    for I in np.arange(0.,620.,20.):
        restore()
        I_pulse = TimedArray(
            [I, I, I, I, I]*pamp,
            dt=200*ms
        )
        run(sim_time)
        frstnrb.append(np.mean(spikemonitorSTNRB.count/sim_time))
        frstnllrs.append(np.mean(spikemonitorSTNLLRS.count/sim_time))
        frstnnr.append(np.mean(spikemonitorSTNNR.count/sim_time))
        frgpea.append(np.mean(spikemonitorGPeA.count/sim_time))
        frgpeb.append(np.mean(spikemonitorGPeB.count/sim_time))
        frgpec.append(np.mean(spikemonitorGPeC.count/sim_time))
        print(f"Processo {k} completato!\n")
        k += 1

    I = np.arange(-300., 620., 20.)*pamp

    plt.figure("f-I curve STN")
    plt.title("f-I curve STN")
    plt.ylabel("spikes/second")
    plt.xlabel("I [pA]")
    plt.plot(I/pamp, frstnrb, 'b', label='RB')
    plt.plot(I/pamp, frstnllrs, 'g', label='LLRS')
    plt.plot(I/pamp, frstnnr, 'y', label='NR')
    plt.legend()

    plt.figure("f-I curve GPe")
    plt.title("f-I curve GPe")
    plt.ylabel("spikes/second")
    plt.xlabel("I [pA]")
    plt.plot(I/pamp, frgpea, 'b', label='A')
    plt.plot(I/pamp, frgpeb, 'g', label='B')
    plt.plot(I/pamp, frgpec, 'y', label='C')
    plt.legend()
    plt.show()


def negpulse():
    restore()
    I_pulse = TimedArray(
        [I, 0, 0, 0, 0]*pamp,
        dt=200*ms
    )

    run(sim_time)

    t = arange(int(sim_time/deft))*deft

    plt.figure("STN Plot")
    plt.subplot(311)
    plt.title(f"STN neuron voltages; Pulse: {I} pA")
    plt.ylabel("v [mV]")
    plt.plot(t/ms, statemonitorSTNRB.v[0]/mV, 'r', label="STN RB")
    plt.legend()
    plt.subplot(312)
    plt.ylabel("v [mV]")
    plt.plot(t/ms, statemonitorSTNLLRS.v[0]/mV, 'g', label="STN LLRS")
    plt.legend()
    plt.subplot(313)
    plt.ylabel("v [mV]")
    plt.xlabel("t [ms]")
    plt.plot(t/ms, statemonitorSTNNR.v[0]/mV, 'b', label="STN NR")
    plt.legend()

    plt.figure("GPe Plot")
    plt.subplot(311)
    plt.title(f"GPe neuron voltages; Pulse: {I} pA")
    plt.ylabel("v [mV]")
    plt.plot(t/ms, statemonitorGPeA.v[0]/mV, 'r', label="GPe A")
    plt.legend()
    plt.subplot(312)
    plt.ylabel("v [mV]")
    plt.plot(t/ms, statemonitorGPeB.v[0]/mV, 'g', label="GPe B")
    plt.legend()
    plt.subplot(313)
    plt.ylabel("v [mV]")
    plt.xlabel("t [ms]")
    plt.plot(t/ms, statemonitorGPeC.v[0]/mV, 'b', label="GPe C")
    plt.legend()
    plt.show()

def pospulse():
    restore()
    I_pulse = TimedArray(
        [I, I, I, I, I]*pamp,
        dt=200*ms
    )

    run(sim_time)

    t = arange(int(sim_time/deft))*deft

    plt.figure("STN Plot")
    plt.subplot(311)
    plt.title(f"STN neuron voltages; Pulse Amplitude: {I} pA")
    plt.ylabel("v [mV]")
    plt.plot(t/ms, statemonitorSTNRB.v[0]/mV, 'r', label="STN RB")
    plt.legend()
    plt.subplot(312)
    plt.ylabel("v [mV]")
    plt.plot(t/ms, statemonitorSTNLLRS.v[5]/mV, 'g', label="STN LLRS")
    plt.legend()
    plt.subplot(313)
    plt.ylabel("v [mV]")
    plt.xlabel("t [ms]")
    plt.plot(t/ms, statemonitorSTNNR.v[0]/mV, 'b', label="STN NR")
    plt.legend()

    plt.figure("GPe Plot")
    plt.subplot(311)
    plt.title(f"GPe neuron voltages; Pulse Amplitude: {I} pA")
    plt.ylabel("v [mV]")
    plt.plot(t/ms, statemonitorGPeA.v[0]/mV, 'r', label="GPe A")
    plt.legend()
    plt.subplot(312)
    plt.ylabel("v [mV]")
    plt.plot(t/ms, statemonitorGPeB.v[0]/mV, 'g', label="GPe B")
    plt.legend()
    plt.subplot(313)
    plt.ylabel("v [mV]")
    plt.xlabel("t [ms]")
    plt.plot(t/ms, statemonitorGPeC.v[0]/mV, 'b', label="GPe C")
    plt.legend()
    plt.show()

sim_time = 1000*ms
I = 0.
pospulse()
print(f"RB --> {np.mean(spikemonitorSTNRB.count)}")
print(f"LLRS --> {np.mean(spikemonitorSTNLLRS.count)}")
print(f"NR --> {np.mean(spikemonitorSTNNR.count)}")