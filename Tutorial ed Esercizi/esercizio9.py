# Neuroni di tipo I e di tipo II
# Plot twist: ti cambia il tipo di biforcazione

import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np
from neurodynex.tools import input_factory, plot_tools, spike_tools
from neurodynex.neuron_type import neurons

"""
# Mi serve una corrente a scalino da 50 ms a 150 ms di intensità 0.5 pA
input_current = input_factory.get_step_current(100, 1100, 1.*b2.ms, 0.38*b2.pA)
neuronX = neurons.NeuronX() # Neurone di tipo I o II
state_monitor1 = neuronX.run(input_current, 1200*b2.ms)
neurons.plot_data(state_monitor1, title="Neurone di tipo X")

neuronY = neurons.NeuronY()
state_monitor2 = neuronY.run(input_current, 1200*b2.ms)
neurons.plot_data(state_monitor2, title="Neurone di tipo Y")


Il tipo dei due neuroni viene randomizzato ad ogni iterazione,
la corrente di soglia per ottenere un firing tonico in entrambi
è di 0.38 pAmp, quindi è con questa corrente che ho la biforcazione
saddle-note onto/off limit cycle.
"""

T = 1200*b2.ms
f1 = []
f2 = []
I = []
I_ist = 0.01

neuronX = neurons.NeuronX()
neuronY = neurons.NeuronY()



while I_ist < 0.90:
    input_current = input_factory.get_step_current(100, 1100, b2.ms, I_ist*b2.pA)
    state_monitor1 = neuronX.run(input_current, T)
    state_monitor2 = neuronY.run(input_current, T)
    spike_stats1 = spike_tools.get_spike_stats(state_monitor1, 0*b2.mV)
    spike_stats2 = spike_tools.get_spike_stats(state_monitor2, 0*b2.mV)
    f1.append(spike_stats1[0]/T)
    f2.append(spike_stats2[0]/T)
    I_ist += 0.01
    I.append(I_ist)

"""
print(f1)
print(f2)
print(I)
"""

plt.figure(1)
plt.xlabel("Current (pAmp)")
plt.ylabel("Firing rate (Hz)")
plt.plot(I,f1)

plt.figure(2)
plt.xlabel("Current (pAmp)")
plt.ylabel("Firing rate (Hz)")
plt.plot(I,f2)

plt.show()


"""
print("Il numero di spike del neurone X è {}".format(spike_stats1[0]))
print("Il numero di spike del neurone Y è {}".format(spike_stats2[0]))
print("Il firing rate del neurone X è {}".format(spike_stats1[0]/T))
print("Il firing rate del neurone Y è {}".format(spike_stats2[0]/T))
"""

# Il neurone X è di tipo 2 mentre il neurone Y è di tipo 1, yay!
