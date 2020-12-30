import matplotlib.pyplot as plt

from brian2 import *
import numpy as np

# Fix seed for reproducible results
seed(42)

N_var = [10, 50, 150, 500, 1000]
c_var = [0.0, 0.02, 0.04, 0.06, 0.08, 0.1]

for j, N in enumerate(N_var):
    # Vary the correlation within the group
    print(f'Il numero di neuroni è {N}')
    for i, c in enumerate(c_var):

        # N = 10            # Number of neuron in the group
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
        start_interval = 0*ms
        end_interval = 4*ms

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
        print(f"Il fano factor calcolato con un time interval di {(end_interval-start_interval)/ms} ms è: {fano_factor}")

    print("\n")