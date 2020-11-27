""" This is the code needed to simulate
    the GPe-STN Loop. Here I'm using the
    Brian2 framework.

    The model proposed is inspired by Izhikevich 2003/2007a,
    and it has been modified by Z. Fountas for a take on Action Selection modelling.
"""
from brian2 import *
#clear_cache('cython')

import argparse
from os import path
import random as ran
import numpy as np
from scipy.signal import butter, welch, filtfilt
from scipy.integrate import simps
from pandas import DataFrame
from entropy import spectral_entropy
import time

from parameters import *
from equations import *
from groupsandsynapses import *
from testfunctions import *


########################### My arguments ##################################################################################################
parser = argparse.ArgumentParser(description="First loop simulation. GPe-STN")
parser.add_argument("serverorlocal", help="Are you simulating on the server or in local machine?", type=str, choices=["server", "local"])
parser.add_argument("controlorpd", help="Do you want to simulate control or pd state?", type=str, choices=["control", "pd"])
parser.add_argument("-g", help="Use general paths.", action="count")
parser.add_argument("-wherecsv", help="Where to save data?", type=str)
args = parser.parse_args()
###########################################################################################################################################

if args.serverorlocal == "server":
    gen_path = "/home/f_mastellone/"
elif args.serverorlocal == "local":
    gen_path = "/home/fvm/Scrivania/"

if args.g == 1:
    final_path_data = gen_path
else:
    final_path_data = path.join(gen_path, args.wherecsv)

if args.controlorpd == "control":
    Dop1 = Dop2 = 0.
elif args.controlorpd == "pd":
    Dop1 = Dop2 = 0.8


def getdata():
    ########################## Initial time to make my network settle down ######################
    run(300*ms)
    ##############################################################################################

    print(f"Freq input CTX = {rate_CTX} Hz\nFreq input STR = {rate_STR} Hz\n")

    """ Functions to monitor neurons' state
    """
    spikemonitorSTN = SpikeMonitor(STNGroup, variables=['v'])
    statemonitorSTN = StateMonitor(STNGroup, ['v','I_lfp_stn', 'I_chem_GPe_STN'], record=True)

    statemonitorSTNRB = StateMonitor(STNRBGroup, ['v'], record=True)
    spikemonitorSTNRB = SpikeMonitor(STNRBGroup, variables=['v'])

    statemonitorSTNLLRS = StateMonitor(STNLLRSGroup, ['v'], record=True)
    spikemonitorSTNLLRS = SpikeMonitor(STNLLRSGroup, variables=['v'])

    statemonitorSTNNR = StateMonitor(STNNRGroup, ['v'], record=True)
    spikemonitorSTNNR = SpikeMonitor(STNNRGroup, variables=['v'])
    
    spikemonitorGPe = SpikeMonitor(GPeGroup, variables=['v'])
    statemonitorGPe = StateMonitor(GPeGroup, ['v','I_lfp_gpe', 'I_chem_STN_GPe'], record=True)
    
    statemonitorGPeA = StateMonitor(GPeAGroup, variables=['v'], record=True)
    spikemonitorGPeA = SpikeMonitor(GPeAGroup, variables=['v'])
    
    statemonitorGPeB = StateMonitor(GPeBGroup, variables=['v'], record=True)
    spikemonitorGPeB = SpikeMonitor(GPeBGroup, variables=['v'])
    
    statemonitorGPeC = StateMonitor(GPeCGroup, variables=['v'], record=True)
    spikemonitorGPeC = SpikeMonitor(GPeCGroup, variables=['v'])
    
    spikemonitorCTX = SpikeMonitor(CorticalGroup)

    ##############################################################################################
    run(duration) # Run boy, run!
    ##############################################################################################

    """ Calculating the Firing Rates for the entire simulation
    """
    
    frGPe = firingrate(spikemonitorGPe, duration)
    frGPeA = firingrate(spikemonitorGPeA, duration)
    frGPeB = firingrate(spikemonitorGPeB, duration)
    frGPeC = firingrate(spikemonitorGPeC, duration)
    
    frSTN = firingrate(spikemonitorSTN, duration)
    frSTNRB = firingrate(spikemonitorSTNRB, duration)
    frSTNLLRS = firingrate(spikemonitorSTNLLRS, duration)
    frSTNNR = firingrate(spikemonitorSTNNR, duration)

    frCTX = firingrate(spikemonitorCTX, duration)

    frGPe = np.mean(frGPe)
    frGPeA = np.mean(frGPeA)
    frGPeB = np.mean(frGPeB)
    frGPeC = np.mean(frGPeC)

    frGPe_std = np.std(frGPe)
    frGPeA_std = np.std(frGPeA)
    frGPeB_std = np.std(frGPeB)
    frGPeC_std = np.std(frGPeC)

    frSTN = np.mean(frSTN)
    frSTNRB = np.mean(frSTNRB)
    frSTNLLRS = np.mean(frSTNLLRS)
    frSTNNR = np.mean(frSTNNR)

    frSTNs = np.std(frSTN)
    frSTNRBs = np.std(frSTNRB)
    frSTNLLRSs = np.std(frSTNLLRS)
    frSTNNRs = np.std(frSTNNR)
    
    """ Calculating ISI, mean ISI and standard deviation of ISI
        for each population.
    """
    isiSTN, mean_isiSTN, std_isiSTN = isi_mean_std(spikemonitorSTN)
    isiSTNRB, mean_isiSTNRB, std_isiSTNRB = isi_mean_std(spikemonitorSTNRB)
    isiSTNLLRS, mean_isiSTNLLRS, std_isiSTNLLRS = isi_mean_std(spikemonitorSTNLLRS)
    isiSTNNR, mean_isiSTNNR, std_isiSTNNR = isi_mean_std(spikemonitorSTNNR)

    isiGPe, mean_isiGPe, std_isiGPe = isi_mean_std(spikemonitorGPe)
    isiGPeA, mean_isiGPeA, std_isiGPeA = isi_mean_std(spikemonitorGPeA)
    isiGPeB, mean_isiGPeB, std_isiGPeB = isi_mean_std(spikemonitorGPeB)
    isiGPeC, mean_isiGPeC, std_isiGPeC = isi_mean_std(spikemonitorGPeC)
    

    """ Calculating Coefficient of Variation:
        How irregular is the firing of my network?
    """
    cv_gpe = coeffvar(std_isiGPe, mean_isiGPe)
    cv_gpea = coeffvar(std_isiGPeA, mean_isiGPeA)
    cv_gpeb = coeffvar(std_isiGPeB ,mean_isiGPeB)
    cv_gpec = coeffvar(std_isiGPeC, mean_isiGPeC)

    cv_stn = coeffvar(std_isiSTN, mean_isiSTN)
    cv_stnrb = coeffvar(std_isiSTNRB, mean_isiSTNRB)
    cv_stnllrs = coeffvar(std_isiSTNLLRS, mean_isiSTNLLRS)
    cv_stnnr = coeffvar(std_isiSTNNR, mean_isiSTNNR)


    """ Calculating meaning currents: mean excitatory and inhibitory current and mean currents to STN and GPe
    """
    mean_I_lfp_STN = np.mean(statemonitorSTN.I_lfp_stn, 0)
    mean_I_lfp_GPe = np.mean(statemonitorGPe.I_lfp_gpe, 0)


    """ Calculating spectra of LFP currents I obtained before
        This is done via scipy.signal.welch and scipy.integrate.simps
    """
    filtered_lfp_STN = butter_bandpass_filter(mean_I_lfp_STN, 1, 100, 1/deft, order=3)
    filtered_lfp_GPe = butter_bandpass_filter(mean_I_lfp_GPe, 1, 100, 1/deft, order=3)

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


    """ Spectral Entropy of nuclei:
        How much peaked and concentrated is my beta band spectrum?
    """
    specentropy_stn = spectral_entropy(filtered_lfp_STN, sf=1/deft, method='welch', nperseg=2/deft, normalize=True)
    specentropy_gpe = spectral_entropy(filtered_lfp_GPe, sf=1/deft, method='welch', nperseg=2/deft, normalize=True)
    


    """ Piece of code to calculate the synchronization between neuron in a single population
        and among the three populations of GPe and STN.
    """
    var_time_v_GPe = variance_time_fluctuations_v(statemonitorGPe)
    norm_GPe = variance_time_flu_v_norm(N_GPe, statemonitorGPe)
    sync_par_GPe = sqrt(var_time_v_GPe / norm_GPe)

    var_time_v_STN = variance_time_fluctuations_v(statemonitorSTN)
    norm_STN = variance_time_flu_v_norm(N_STN, statemonitorSTN)
    sync_par_STN = sqrt(var_time_v_STN / norm_STN)
    
    var_time_v_GPeA = variance_time_fluctuations_v(statemonitorGPeA)
    norm_GPeA = variance_time_flu_v_norm(N_GPe_A, statemonitorGPeA)
    sync_par_GPeA = sqrt(var_time_v_GPeA / norm_GPeA)

    var_time_v_GPeB = variance_time_fluctuations_v(statemonitorGPeB)
    norm_GPeB = variance_time_flu_v_norm(N_GPe_B, statemonitorGPeB)
    sync_par_GPeB = sqrt(var_time_v_GPeB / norm_GPeB)

    var_time_v_GPeC = variance_time_fluctuations_v(statemonitorGPeC)
    norm_GPeC = variance_time_flu_v_norm(N_GPe_C, statemonitorGPeC)
    sync_par_GPeC = sqrt(var_time_v_GPeC / norm_GPeC)

    var_time_v_STNRB = variance_time_fluctuations_v(statemonitorSTNRB)
    norm_STNRB = variance_time_flu_v_norm(N_STN_RB, statemonitorSTNRB)
    sync_par_STNRB = sqrt(var_time_v_STNRB / norm_STNRB)

    var_time_v_STNLLRS = variance_time_fluctuations_v(statemonitorSTNLLRS)
    norm_STNLLRS = variance_time_flu_v_norm(N_STN_LLRS, statemonitorSTNLLRS)
    sync_par_STNLLRS = sqrt(var_time_v_STNLLRS / norm_STNLLRS)

    var_time_v_STNNR = variance_time_fluctuations_v(statemonitorSTNNR)
    norm_STNNR = variance_time_flu_v_norm(N_STN_NR, statemonitorSTNNR)
    sync_par_STNNR = sqrt(var_time_v_STNNR / norm_STNNR)
    
        
    """ Space reserved to plot useful stuff down here.
    """
    '''
    plt.figure(1)
    plt.subplot(311)
    plt.title(f'Membrane Potential; CTX: {rate_CTX} Hz STR: {rate_STR} Hz')
    plt.ylabel('v [mV]')
    plt.plot(t_recorded/ms, statemonitorSTNRB.v[0]/mV, 'r', label='STN RB')
    plt.legend()
    plt.subplot(312)
    plt.ylabel('v [mV]')
    plt.plot(t_recorded/ms, statemonitorSTNLLRS.v[0]/mV, 'g', label='STN LLRS')
    plt.legend()
    plt.subplot(313)
    plt.ylabel('v [mV]')
    plt.xlabel('Time [ms]')
    plt.plot(t_recorded/ms, statemonitorSTNNR.v[0]/mV, 'b', label='STN NR')
    plt.legend()

    plt.figure(2)
    plt.subplot(311)
    plt.title(f'Membrane Potential; CTX: {rate_CTX} Hz STR: {rate_STR} Hz')
    plt.ylabel('v [mV]')
    plt.plot(t_recorded/ms, statemonitorGPeA.v[0]/mV, 'r', label='GPe A')
    plt.legend()
    plt.subplot(312)
    plt.ylabel('v [mV]')
    plt.plot(t_recorded/ms, statemonitorGPeB.v[0]/mV, 'g', label='GPe B')
    plt.legend()
    plt.subplot(313)
    plt.ylabel('v [mV]')
    plt.xlabel('Time [ms]')
    plt.plot(t_recorded/ms, statemonitorGPeC.v[0]/mV, 'b', label='GPe C')
    plt.legend()

    
    plt.figure(3)
    plt.subplot(211)
    plt.title(f'Plot Correnti; CTX: {rate_CTX} Hz STR: {rate_STR} Hz')
    plt.ylabel('I [pA]')
    plt.plot(t_recorded/ms, statemonitorSTN.I_chem_GPe_STN[22]/pamp, 'b', label='GPe --> STN')
    plt.legend()
    plt.subplot(212)
    plt.ylabel('I [pA]')
    plt.xlabel('t [ms]')
    plt.plot(t_recorded/ms, statemonitorGPe.I_chem_STN_GPe[54]/pamp, 'g', label='STN --> GPe')
    plt.legend()
    '''

    
    """ Retrieving data I need for analysis
    """
    data_provv = [rate_CTX, rate_STR, frGPe, frGPeA, frGPeB, frGPeC, frSTN,
    frSTNRB, frSTNLLRS, frSTNNR, cv_gpe, cv_gpea, cv_gpeb, cv_gpec, cv_stn, cv_stnrb, 
    cv_stnllrs, cv_stnnr, beta_power_stn/total_power_stn, beta_power_gpe/total_power_gpe,
    specentropy_stn, specentropy_gpe, sync_par_STNRB, sync_par_STNLLRS, sync_par_STNNR, sync_par_STN,
    sync_par_GPeA, sync_par_GPeB, sync_par_GPeC, sync_par_GPe]

    data_provv = np.asarray(data_provv)
    return data_provv
    
    

data = np.asarray(['Rate CTX', 'Rate STR', 'F.R. GPe', 'F.R. GPe A','F.R. GPe B','F.R. GPe C', 'F.R. STN',
'F.R. STN RB','F.R. STN LLRS','F.R. STN NR','CV GPe', 'CV GPe A','CV GPe B','CV GPe C', 'CV STN',
'CV STN RB','CV STN LLRS','CV STN NR', 'Beta % STN', 'Beta % GPe', 'Spectral Entropy STN', 'Spectral Entropy GPe',
'Sync. Param. STN RB', 'Sync. Param. STN LLRS', 'Sync. Param. STN NR', 'Sync. Param. STN',
'Sync. Param. GPe A', 'Sync. Param. GPe B', 'Sync. Param. GPe C', 'Sync. Param. GPe'])

rates_CTX = np.arange(3., 11., 1.)
rates_STR_1 = np.array([0.01, 0.1, 0.5, 1., 1.5, 2.])
rates_STR_2 = np.arange(17., 49., 1.)
rates_STR = np.hstack((rates_STR_1, rates_STR_2))

k = 1 # Index to watch my processes

print("Processes started.\n")

t1 = time.time()

############################## Caratterizzazione BlackBox ################
for i in rates_CTX:
    for j in rates_STR:
        t2 = time.time()
        rate_CTX = i*Hz
        rate_STR = j*Hz
        CorticalGroup.rates = rate_CTX
        StriatalGroup.rates = rate_STR

        data_provv = getdata()
        data = np.vstack((data,data_provv))
        t3 = time.time()
        print(f"Process {k} finished in {(t3 - t2)/60} minutes.\n\n\n")
        k += 1
############################################################################


dataframe = DataFrame(data=data[1:], columns=data[0,:])
dataframe.to_csv(f'{final_path_data}/data.csv', index=False)

t4 = time.time()

print(f"Process finished successfully in {(t4-t1)/60} minutes.")