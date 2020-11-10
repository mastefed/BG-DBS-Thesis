""" This is the code needed to simulate
    the GPe-STN Loop. Here I'm using the
    Brian2 framework.

    The model proposed is inspired by Izhikevich 2003/2007a,
    and it has been modified by Z. Fountas for a take on Action Selection modelling.
"""

from brian2 import *
import random as ran
import numpy as np
from scipy.signal import butter, welch, filtfilt
from scipy.integrate import simps
from parameters import *
from equations import *
from groupsandsynapses import *
from testfunctions import *

def main():
    run(300*ms)

    print(f"Freq input STR = {rate_STR}, Freq input CTX = {rate_CTX}\n")

    """ Functions to monitor neurons' state
    """
    spikemonitorSTNRB = SpikeMonitor(STNRBGroup, variables=['v'])
    statemonitorSTNRB = StateMonitor(STNRBGroup, ['v','I_lfp_stnrb'], record=True)

    spikemonitorSTNLLRS = SpikeMonitor(STNLLRSGroup, variables=['v'])
    statemonitorSTNLLRS = StateMonitor(STNLLRSGroup, ['v','I_lfp_stnllrs'], record=True)

    spikemonitorSTNNR = SpikeMonitor(STNNRGroup, variables=['v'])
    statemonitorSTNNR = StateMonitor(STNNRGroup, ['v','I_lfp_stnnr'], record=True)

    spikemonitorGPeA = SpikeMonitor(GPeAGroup, variables=['v'])
    statemonitorGPeA = StateMonitor(GPeAGroup, ['v','I_lfp_gpea'], record=True)

    spikemonitorGPeB = SpikeMonitor(GPeBGroup, variables=['v'])
    statemonitorGPeB = StateMonitor(GPeBGroup, ['v','I_lfp_gpeb'], record=True)

    spikemonitorGPeC = SpikeMonitor(GPeCGroup, variables=['v'])
    statemonitorGPeC = StateMonitor(GPeCGroup, ['v','I_lfp_gpec'], record=True)

    spikemonitorCTX = SpikeMonitor(CorticalGroup)

    populationSTNRB = PopulationRateMonitor(STNRBGroup)
    populationSTNLLRS = PopulationRateMonitor(STNLLRSGroup)
    populationSTNNR = PopulationRateMonitor(STNNRGroup)

    populationGPeA = PopulationRateMonitor(GPeAGroup)
    populationGPeB = PopulationRateMonitor(GPeBGroup)
    populationGPeC = PopulationRateMonitor(GPeCGroup)

    run(duration) # Run boy, run!

    """ Calculating the Firing Rates for the entire simulation
    """
    frGPeA = firingrate(spikemonitorGPeA, duration)
    frGPeB = firingrate(spikemonitorGPeB, duration)
    frGPeC = firingrate(spikemonitorGPeC, duration)
    frSTNRB = firingrate(spikemonitorSTNRB, duration)
    frSTNLLRS = firingrate(spikemonitorSTNLLRS, duration)
    frSTNNR = firingrate(spikemonitorSTNNR, duration)
    frCTX = firingrate(spikemonitorCTX, duration)

    frGPeA = np.mean(frGPeA)
    frGPeB = np.mean(frGPeB)
    frGPeC = np.mean(frGPeC)
    frSTNRB = np.mean(frSTNRB)
    frSTNNR = np.mean(frSTNNR)
    frSTNLLRS = np.mean(frSTNLLRS)
    '''
    print(f"La frequenza f dell'input rate della CTX è: {input_rates(416*ms)}\n")
    print(f"Il firing rate della CTX è: {np.mean(frCTX)} Hz\n")
    print(f"Il firing rate del GPe A è: {np.mean(frGPeA)} Hz\n")
    print(f"Il firing rate del GPe B è: {np.mean(frGPeB)} Hz\n")
    print(f"Il firing rate del GPe C è: {np.mean(frGPeC)} Hz\n")
    print(f"Il firing rate del STN RB è: {np.mean(frSTNRB)} Hz\n")
    print(f"Il firing rate del STN LLRS è: {np.mean(frSTNLLRS)} Hz\n")
    print(f"Il firing rate del STN NR è: {np.mean(frSTNNR)} Hz\n")
    '''
    mean_isiGPeA, std_isiGPeA = isi_mean_std(spikemonitorGPeA, 0)
    mean_isiGPeB, std_isiGPeB = isi_mean_std(spikemonitorGPeB, 2)
    mean_isiGPeC, std_isiGPeC = isi_mean_std(spikemonitorGPeC, 1)
    mean_isiSTNRB, std_isiSTNRB = isi_mean_std(spikemonitorSTNRB, 3)
    mean_isiSTNLLRS, std_isiSTNLLRS = isi_mean_std(spikemonitorSTNLLRS, 0)
    mean_isiSTNNR, std_isiSTNNR = isi_mean_std(spikemonitorSTNNR, 1)

    cv_gpea = std_isiGPeA/mean_isiGPeA
    cv_gpeb = std_isiGPeB/mean_isiGPeB
    cv_gpec = std_isiGPeC/mean_isiGPeC
    cv_stnrb = std_isiSTNRB/mean_isiSTNRB
    cv_stnllrs = std_isiSTNLLRS/mean_isiSTNLLRS
    cv_stnnr = std_isiSTNNR/mean_isiSTNNR

    '''
    print("Il coefficiente di variazione per ISI per un neurone di:\n")
    print(f"GPe A {std_isiGPeA/mean_isiGPeA}\n")
    print(f"GPe B {std_isiGPeB/mean_isiGPeB}\n")
    print(f"GPe C {std_isiGPeC/mean_isiGPeC}\n")
    print(f"STN RB {std_isiSTNRB/mean_isiSTNRB}\n")
    print(f"STN LLRS {std_isiSTNLLRS/mean_isiSTNLLRS}\n")
    print(f"STN NR {std_isiSTNNR/mean_isiSTNNR}\n")
    '''
    """ Calculating the Population firing rate over time for STN and GPe
    """
    width = 2.*ms
    populationSTNfr = np.mean([populationSTNRB.smooth_rate(width=width), populationSTNNR.smooth_rate(width=width), populationSTNLLRS.smooth_rate(width=width)], 0)
    populationGPefr = np.mean([populationGPeA.smooth_rate(width=width), populationGPeB.smooth_rate(width=width), populationGPeC.smooth_rate(width=width)], 0)

    """ Calculating meaning currents: mean excitatory and inhibitory current and mean currents to STN and GPe
    """
    mean_I_lfp_STNRB = np.mean(statemonitorSTNRB.I_lfp_stnrb, 0)
    mean_I_lfp_STNLLRS = np.mean(statemonitorSTNLLRS.I_lfp_stnllrs, 0)
    mean_I_lfp_STNNR = np.mean(statemonitorSTNNR.I_lfp_stnnr, 0)
    mean_I_lfp_GPeA = np.mean(statemonitorGPeA.I_lfp_gpea, 0)
    mean_I_lfp_GPeB = np.mean(statemonitorGPeB.I_lfp_gpeb, 0)
    mean_I_lfp_GPeC = np.mean(statemonitorGPeC.I_lfp_gpec, 0)

    mean_I_lfp_STN = np.vstack((mean_I_lfp_STNRB, mean_I_lfp_STNLLRS, mean_I_lfp_STNNR))
    mean_I_lfp_STN = np.mean(mean_I_lfp_STN, 0)
    mean_I_lfp_GPe = np.vstack((mean_I_lfp_GPeA, mean_I_lfp_GPeB, mean_I_lfp_GPeC))
    mean_I_lfp_GPe = np.mean(mean_I_lfp_GPe, 0)

    filtered_lfp_STN = butter_bandpass_filter(mean_I_lfp_STN, 1, 100, 1/deft, order=3)
    filtered_lfp_GPe = butter_bandpass_filter(mean_I_lfp_GPe, 1, 100, 1/deft, order=3)

    #printcurrents(3, "LFP STN (red) GPe (green)", [filtered_lfp_STN, filtered_lfp_GPe], ['r', 'g'])

    fstn, specstn = welch(filtered_lfp_STN, fs=1/deft, nperseg=2/deft, nfft=2**18)
    fgpe, specgpe = welch(filtered_lfp_GPe, fs=1/deft, nperseg=2/deft, nfft=2**18)
    low = 12*Hz
    high = 38*Hz
    idx_beta_stn = np.logical_and(fstn >= low, fstn <= high)
    idx_beta_gpe = np.logical_and(fgpe >= low, fgpe <= high)

    freq_res_stn = fstn[1] - fstn[0]
    freq_res_gpe = fgpe[1] - fgpe[0]
    total_power_stn = simps(specstn, dx=freq_res_stn)
    total_power_gpe = simps(specgpe, dx=freq_res_gpe)
    beta_power_stn = simps(specstn[idx_beta_stn], dx=freq_res_stn)
    beta_power_gpe = simps(specgpe[idx_beta_gpe], dx=freq_res_gpe)

    pdf_stn = beta_power_stn/total_power_stn
    pdf_gpe = beta_power_gpe/total_power_gpe

    specentropy_stn = - pdf_stn * np.log(pdf_stn)
    specentropy_gpe = - pdf_gpe * np.log(pdf_gpe)

    print(f"Normalized Beta Power for STN {beta_power_stn/total_power_stn}\n")
    print(f"Normalized Beta Power for GPe {beta_power_gpe/total_power_gpe}\n")
        
    plt.figure(x)
    plt.title("Spectral density LFP STN (green) LFP GPe (red)")
    plt.xlabel("Frequencies (Hz)")
    plt.xlim(0,50)
    plt.fill_between(fstn, specstn, where=idx_beta_stn, color='c')
    plt.fill_between(fgpe, specgpe, where=idx_beta_gpe, color='m')
    plt.plot(fgpe, specgpe, 'r')
    plt.plot(fstn, specstn, 'g')
        
    plt.show()

    data_provv = [rate_CTX, rate_STR, frGPeA, frGPeB, frGPeC, 
    frSTNRB, frSTNLLRS, frSTNNR, cv_gpea, cv_gpeb, cv_gpec, cv_stnrb, 
    cv_stnllrs, cv_stnnr, beta_power_stn/total_power_stn, beta_power_gpe/total_power_gpe,
    specentropy_stn, specentropy_gpe]

    data_provv = np.asarray(data_provv)
    data = np.vstack(data_provv)


    
data = np.asarray(['Rate CTX','Rate STR','F.R. GPe A','F.R. GPe B','F.R. GPe C',
'F.R. STN RB','F.R. STN LLRS','F.R. STN RB','CV GPe A','CV GPe B','CV GPe C',
'CV STN RB','CV STN LLRS','CV STN NR', 'Beta % STN', 'Beta % GPe', 'Spec Entropy STN', 
'Spec Entropy GPe'])


for y in rates_STR:
    rate_STR = y*Hz
    for x in rates_CTX:
        rate_CTX = x*Hz
        main()

print(data)