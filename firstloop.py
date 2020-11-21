""" This is the code needed to simulate
    the GPe-STN Loop. Here I'm using the
    Brian2 framework.

    The model proposed is inspired by Izhikevich 2003/2007a,
    and it has been modified by Z. Fountas for a take on Action Selection modelling.
"""

import argparse
from os import path
from brian2 import *
import random as ran
import numpy as np
from scipy.signal import butter, welch, filtfilt
from scipy.integrate import simps
from pandas import DataFrame
from entropy import spectral_entropy
from parameters import *
from equations import *
from groupsandsynapses import *
from testfunctions import *

parser = argparse.ArgumentParser(description="First loop simulation. GPe-STN")
parser.add_argument("serverorlocal", help="Are you simulating on the server or in local machine?", type=str, choices=["server", "local"])
parser.add_argument("-g", help="Use general paths.", action="count")
parser.add_argument("-wherecsv", help="Where to save data?", type=str)
parser.add_argument("-whereimgs", help="Where to save imgs?", type=str)
args = parser.parse_args()

print("Hey oh 1")

if args.serverorlocal == "server":
    gen_path = "/home/f_mastellone/"
elif args.serverorlocal == "local":
    gen_path = "/home/fvm/Scrivania/"

if args.g == 1:
    final_path_data = gen_path
    final_path_images = gen_path
else:
    final_path_data = path.join(gen_path, args.wherecsv)
    final_path_images = path.join(gen_path, args.whereimgs)

print("Hey oh 2")


def getdata():
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

    populationCTX = PopulationRateMonitor(CorticalGroup)
    populationSTR = PopulationRateMonitor(StriatalGroup)

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

    """ Calculating the Population firing rate over time for STN and GPe
    """
    width = 2.*ms
    populationSTNfr = np.mean([populationSTNRB.smooth_rate(width=width), populationSTNNR.smooth_rate(width=width), populationSTNLLRS.smooth_rate(width=width)], 0)
    populationGPefr = np.mean([populationGPeA.smooth_rate(width=width), populationGPeB.smooth_rate(width=width), populationGPeC.smooth_rate(width=width)], 0)

    print(f"Cortical Pop. Rate over time --> {populationCTX.smooth_rate(width=width)}\n")
    print(f"Striatal Pop. Rate over time --> {populationSTR.smooth_rate(width=width)}\n")

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

    specentropy_stn = spectral_entropy(filtered_lfp_STN, sf=1/deft, method='welch', nperseg=2/deft, normalize=True)
    specentropy_gpe = spectral_entropy(filtered_lfp_GPe, sf=1/deft, method='welch', nperseg=2/deft, normalize=True)
    
    """ Piece of code to calculate the synchronization between neuron in a single population
        and among the three populations of GPe and STN.
    """
    var_time_v_GPeA = variance_time_fluctuations_v(statemonitorGPeA)
    norm_GPeA = variance_time_flu_v_norm(N_GPe_A, statemonitorGPeA)
    sync_par_GPeA = sqrt(var_time_v_GPeA / norm_GPeA)
    #print(f"Il parametro di sincronizzazione per il GPe A è {sync_par_GPeA}\n")

    var_time_v_GPeB = variance_time_fluctuations_v(statemonitorGPeB)
    norm_GPeB = variance_time_flu_v_norm(N_GPe_B, statemonitorGPeB)
    sync_par_GPeB = sqrt(var_time_v_GPeB / norm_GPeB)
    #print(f"Il parametro di sincronizzazione per il GPe B è {sync_par_GPeB}\n")

    var_time_v_GPeC = variance_time_fluctuations_v(statemonitorGPeC)
    norm_GPeC = variance_time_flu_v_norm(N_GPe_C, statemonitorGPeC)
    sync_par_GPeC = sqrt(var_time_v_GPeC / norm_GPeC)
    #print(f"Il parametro di sincronizzazione per il GPe C è {sync_par_GPeC}\n")

    var_time_v_STNRB = variance_time_fluctuations_v(statemonitorSTNRB)
    norm_STNRB = variance_time_flu_v_norm(N_STN_RB, statemonitorSTNRB)
    sync_par_STNRB = sqrt(var_time_v_STNRB / norm_STNRB)
    #print(f"Il parametro di sincronizzazione per il STN RB è {sync_par_STNRB}\n")

    var_time_v_STNLLRS = variance_time_fluctuations_v(statemonitorSTNLLRS)
    norm_STNLLRS = variance_time_flu_v_norm(N_STN_LLRS, statemonitorSTNLLRS)
    sync_par_STNLLRS = sqrt(var_time_v_STNLLRS / norm_STNLLRS)
    #print(f"Il parametro di sincronizzazione per il STN LLRS è {sync_par_STNLLRS}\n")

    var_time_v_STNNR = variance_time_fluctuations_v(statemonitorSTNNR)
    norm_STNNR = variance_time_flu_v_norm(N_STN_NR, statemonitorSTNNR)
    sync_par_STNNR = sqrt(var_time_v_STNNR / norm_STNNR)
    #print(f"Il parametro di sincronizzazione per il STN NR è {sync_par_STNNR}\n")

    var_time_v_GPe = variance_time_fluctuations_v_3pop(statemonitorGPeA, statemonitorGPeB, statemonitorGPeC)
    norm_GPe = variance_time_flu_v_norm_3pop([N_GPe_A, N_GPe_B, N_GPe_C], [statemonitorGPeA, statemonitorGPeB, statemonitorGPeC])
    sync_par_GPe = var_time_v_GPe / norm_GPe
    #print(f"Il parametro di sincronizzazione per l'intero GPe è {sync_par_GPe}\n")

    var_time_v_STN = variance_time_fluctuations_v_3pop(statemonitorSTNRB, statemonitorSTNLLRS, statemonitorSTNNR)
    norm_STN = variance_time_flu_v_norm_3pop([N_STN_RB, N_STN_LLRS, N_STN_NR], [statemonitorSTNRB, statemonitorSTNLLRS, statemonitorSTNNR])
    sync_par_STN = var_time_v_STN / norm_STN
    #print(f"Il parametro di sincronizzazione per l'intero STN è {sync_par_STN}\n")
    
    plt.figure(f"{rate_CTX} + {rate_STR}")
    plt.title(f"PSD LFP STN (g) LFP GPe (r) FR CTX = {rate_CTX} FR STR = {rate_STR}")
    plt.xlabel("Frequencies (Hz)")
    plt.xlim(0,100)
    plt.fill_between(fstn, specstn, where=idx_beta_stn, color='c')
    plt.fill_between(fgpe, specgpe, where=idx_beta_gpe, color='m')
    plt.plot(fgpe, specgpe, 'r')
    plt.plot(fstn, specstn, 'g')
        
    plt.savefig(f"{final_path_images}/RateCTX{rate_CTX}RateSTR{rate_STR}.png")
    plt.close(fig='all')
    '''
    plt.figure(1)
    printpotential("Potenziale (1 neur) GPe B", statemonitorGPeB, "g", 2)
    plt.savefig(f"{final_path_images}/potgpeb.png")
    plt.close()
    '''
    plt.figure(2)
    printpotential("Potenziale (1 neur) STN", statemonitorSTNRB, "r", 3, "STN RB")
    printpotential("Potenziale (1 neur) STN", statemonitorSTNLLRS, "g", 2, "STN LLRS")
    printpotential("Potenziale (1 neur) STN", statemonitorSTNNR, "b", 1, "STN NR")
    plt.savefig(f"{final_path_images}/potstnrb.png")
    plt.show()
    
    data_provv = [rate_CTX, rate_STR, frGPeA, frGPeB, frGPeC, 
    frSTNRB, frSTNLLRS, frSTNNR, cv_gpea, cv_gpeb, cv_gpec, cv_stnrb, 
    cv_stnllrs, cv_stnnr, beta_power_stn/total_power_stn, beta_power_gpe/total_power_gpe,
    specentropy_stn, specentropy_gpe, sync_par_STNRB, sync_par_STNLLRS, sync_par_STNNR, sync_par_STN,
    sync_par_GPeA, sync_par_GPeB, sync_par_GPeC, sync_par_GPe]

    data_provv = np.asarray(data_provv)
    return data_provv
    
    
data = np.asarray(['Rate CTX','Rate STR','F.R. GPe A','F.R. GPe B','F.R. GPe C',
'F.R. STN RB','F.R. STN LLRS','F.R. STN NR','CV GPe A','CV GPe B','CV GPe C',
'CV STN RB','CV STN LLRS','CV STN NR', 'Beta % STN', 'Beta % GPe', 'Spectral Entropy STN', 'Spectral Entropy GPe',
'Sync. Param. STN RB', 'Sync. Param. STN LLRS', 'Sync. Param. STN NR', 'Sync. Param. STN',
'Sync. Param. GPe A', 'Sync. Param. GPe B', 'Sync. Param. GPe C', 'Sync. Param. GPe'])

rates_CTX = np.arange(10.,10.,1.)       #(0., 41., 1.)
rates_STR = np.arange(18.,18.,1.)       #(0., 48., 1.)

print("Hey oh 3")

k = 0

for i in rates_CTX:
    for j in rates_STR:
        rate_CTX = i*Hz
        rate_STR = j*Hz
        CorticalGroup.rates = rate_CTX
        StriatalGroup.rates = rate_STR
        data_provv = getdata()
        data = np.vstack((data,data_provv))
        print(f"Process {k} finished.\n")
        k += 1

dataframe = DataFrame(data=data[1:], columns=data[0,:])
dataframe.to_csv(f'{final_path_data}/data.csv', index=False)
print("Process finished successfully.")