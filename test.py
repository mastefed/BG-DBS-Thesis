import brian2 as b2
import numpy as np

def fanofactor(duration, spikemon, num_neur, start_interval, end_interval):
    """ Funzione per calcolare il Fano Factor
    """
    # Definisco l'inizio e la fine del time bin
    start_interval = start_interval
    end_interval = end_interval

    # Definisco il range su cui iterare
    my_range = int(duration/(end_interval - start_interval))

    average_firing_rates = []

    for k in range(my_range):
        # Definisco il time bin
        time_bin = end_interval - start_interval
        # Prendo tutti gli elementi presi tra due valori
        time_stamps = spikemon.t[(spikemon.t>=start_interval)*(spikemon.t<end_interval)]
        # Mi calcolo il firing rate medio
        average_firing_rate = len(time_stamps) / (num_neur * time_bin)
        average_firing_rates.append(average_firing_rate)
        # Aggiorno l'intervallo
        start_interval += time_bin
        end_interval += time_bin

    fano_factor = np.var(average_firing_rates)/np.mean(average_firing_rates)
    return fano_factor

def variance_time_fluctuations_v(stmonit):
    """Mi serve per calcolare 
    """
    mean_v_pop = np.mean(stmonit.V, 0)
    sigma_2v = np.mean(mean_v_pop**2) - (np.mean(mean_v_pop))**2
    return sigma_2v

def variance_time_flu_v_norm(N_neur, stmonit):
    sigma_2v_tot = 0
    for i in range(N_neur):
        sigma_2v = np.mean(stmonit.V[i]**2) - (np.mean(stmonit.V[i]))**2
        sigma_2v_tot += sigma_2v
    norm = sigma_2v_tot / N_neur
    return norm