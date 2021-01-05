import brian2 as b2
import numpy as np

def fanofactor(duration, spikemon, num_neur, start_interval, end_interval, time_span):
    """ Funzione per calcolare il Fano Factor
    """
    # Definisco il range su cui iterare
    my_range = int(duration/(end_interval - start_interval))

    # Definisco l'inizio e la fine del time bin
    start_interval = start_interval/b2.second
    end_interval = end_interval/b2.second
    time_span = time_span/b2.second

    spike_counts = []

    for k in range(my_range):
        # Definisco il time bin
        time_bin = end_interval - start_interval
        spikemon_no_time = spikemon.t/b2.second
        # Prendo tutti gli elementi presi tra due valori
        time_stamps = spikemon_no_time[np.where((spikemon_no_time>=start_interval)&(spikemon_no_time<end_interval))]
        # Mi calcolo il firing rate medio
        spike_count = len(time_stamps) / num_neur
        spike_counts.append(spike_count)
        # Aggiorno l'intervallo
        start_interval += time_span
        end_interval += time_span

    fano_factor = np.var(spike_counts)/np.mean(spike_counts)
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