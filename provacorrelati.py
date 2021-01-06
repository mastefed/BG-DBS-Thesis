import matplotlib.pyplot as plt

from brian2 import *
import numpy as np

def fanofactor(S, start_interval, end_interval):
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
        time_stamps = S.t[(S.t>=start_interval)*(S.t<end_interval)]
        # Mi calcolo il firing rate medio
        average_firing_rate = len(time_stamps) / (N * time_bin)
        average_firing_rates.append(average_firing_rate)
        # Aggiorno l'intervallo
        start_interval += time_bin
        end_interval += time_bin

    fano_factor = np.var(average_firing_rates)/np.mean(average_firing_rates)
    return fano_factor

# Fix seed for reproducible results
seed(42)

N_var = [10, 50, 150, 500, 1000, 10000]
c_var = [1.]

FF_for_N = {"Number of neurons" : "Array of Fano Factors"}

for j, N in enumerate(N_var):
    # Vary the correlation within the group
    fano_factors = []
    print(f'Il numero di neuroni è {N}')
    for i, c in enumerate(c_var):

        rate = 10 * Hz    # Mean firing rate of each neuron

        # Homogeneous correlated spike trains using thinning of Poisson processes
        # c is the correlation within the group (0 < c < 1)
        # The term "(v < rate*dt) and rand() < sqrt(c))" generates the correlated spikes from the reference spike train
        # The term "rand() < rate*(1 - sqrt(c))*dt" fills out missing spikes to obtain the desired firing rate
        G = NeuronGroup(N, 'v : 1 (shared)', threshold='((v < rate*dt) and rand() < sqrt(c)) or rand() < rate*(1 - sqrt(c))*dt')
        G.run_regularly('v = rand()')  # shared random variable for the reference spike train

        # Run simulation
        duration = 4 * second
        S = SpikeMonitor(G)
        net = Network(G, S)
        net.run(duration)

        # Print informations
        print(f"Il valore di c è {c}")

        # Definisco l'inizio e la fine del time bin
        start_interval = 0.
        end_interval = 0.002

        # Definisco il range su cui iterare
        my_range = int(duration/(end_interval - start_interval))

        average_firing_rates = []

        for k in range(my_range):
            # Definisco il time bin
            time_bin = end_interval - start_interval
            # Prendo tutti gli elementi presi tra due valori
            S_no_time = S.t/second
            time_stamps = S_no_time[np.where((S_no_time>=start_interval)&(S_no_time<end_interval))]
            # Mi calcolo il firing rate medio
            average_firing_rate = len(time_stamps)/N
            average_firing_rates.append(average_firing_rate)
            # Aggiorno l'intervallo
            start_interval += time_bin
            end_interval += time_bin

        fano_factor = np.var(average_firing_rates)/np.mean(average_firing_rates)
        print(f"Il fano factor calcolato con un time interval di {(end_interval-start_interval)/ms} ms è: {fano_factor}")
        fano_factors.append(fano_factor)
        FF_for_N[f"{N}"] = fano_factors
    print("\n")

FF_for_10 = FF_for_N['10']
FF_for_50 = FF_for_N['50']
FF_for_150 = FF_for_N['150']
FF_for_500 = FF_for_N['500']
FF_for_1000 = FF_for_N['1000']
FF_for_10000 = FF_for_N['10000']

plt.figure("Fano Factors")
plt.title("FF for different Neuronal Populations and Correlation Factors")
plt.plot(c_var, FF_for_10, label='10 neurons')
plt.plot(c_var, FF_for_50, label='50 neurons')
plt.plot(c_var, FF_for_150, label='150 neurons')
plt.plot(c_var, FF_for_500, label='500 neurons')
plt.plot(c_var, FF_for_1000, label='1000 neurons')
plt.plot(c_var, FF_for_10000, label='10000 neurons')
plt.xlabel("Correlation Factor")
plt.ylabel("Fano Factor")
plt.legend()

plt.show()