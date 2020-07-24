# Primo esercizio tra quelli proposti

from neurodynex.leaky_integrate_and_fire import LIF
from neurodynex.tools import input_factory, plot_tools
from neurodynex.tools.spike_tools import *
import matplotlib.pyplot as plt
from scipy import signal
from numpy import *

"""
Prima parte dell'esercizio numero 1
Simulare un IF con i parametri di default e create una curva f-I

i_min = 41.26*b2.nA
# i_min = 2.000014*b2.nA
simulation_time=500*b2.ms

# LIF.print_default_parameters()

i_array = np.arange(0, 110, 10)
print(i_array)
fr_array = []

x = range(11)
for n in x:
    # corrente a gradino di valore i_min (da definire)
    step_current = input_factory.get_step_current(t_start=50, t_end=450, unit_time=b2.ms, amplitude=i_array[n]*b2.nA)

    (state_monitor, spike_monitor) = LIF.simulate_LIF_neuron(input_current=step_current, simulation_time=500 * b2.ms)

    # plot_tools.plot_voltage_and_current_traces(state_monitor, step_current, title="min input",
    #                                            firing_threshold=LIF.FIRING_THRESHOLD)
    print("The injected current is: {} nA".format(i_array[n]))
    print("Number of spikes: {}".format(spike_monitor.count[0]))
    print("Simulation time: {} ms".format(simulation_time))
    # print("Il più alto firing rate raggiungibile è 382.0")
    print("Firing rate of the neuron: {} Hz\n".format(spike_monitor.count[0] / simulation_time))

    fr_array.append(spike_monitor.count[0]/simulation_time)

    # plt.show()

plt.figure("f-I curve")
plt.plot(i_array, fr_array, 'g', lw=1)
plt.grid(color='g', ls='--', lw=1)
plt.xlabel("Current (nA)")
plt.ylabel("Firing rate (Hz)")
plt.show()
"""

"""
Seconda parte dell'esercizio numero 1
"""

frequencies = np.arange(10, 110, 10)
amplitude = []
x = 0
t = linspace(0.0, 0.500, 5000, endpoint=False)
dt = linspace(-t[-1], t[-1], 2*5000-1)
phase_shift = []
while x < 10:
    current = input_factory.get_sinusoidal_current(t_start=50,
                                                   t_end=450,
                                                   unit_time=0.1 * b2.ms,
                                                   amplitude=2.5 * b2.nA,
                                                   frequency=frequencies[x]*b2.Hz,
                                                   direct_current=0 * b2.nA,
                                                   phase_offset=0.0,
                                                   append_zero=True)
    y = 0
    pere = []
    while y <= 500:
        pere.append(current(y*0.1*b2.ms, 0))  # Becca l'intera corrente estrapolandola dal TimedArray di Brian2
        y += 0.1
    (state_monit, spike_monit) = LIF.simulate_LIF_neuron(input_current=current,
                                                         simulation_time=500 * b2.ms,
                                                         v_rest=-70 * b2.mV,
                                                         v_reset=-65 * b2.mV,
                                                         firing_threshold=-50 * b2.mV,
                                                         membrane_resistance=10 * b2.Mohm,
                                                         membrane_time_scale=8 * b2.msecond,
                                                         abs_refractory_period=1 * b2.msecond)
    # print("L'ampiezza massima è: {} volt".format(max(state_monit.v[0]) - min(state_monit.v[0])))
    amplitude.append(max(state_monit.v[0]))
    corr = signal.correlate(state_monit.v[0], pere, mode='full')
    # print("Il massimo della funzione di cross-correlazione è {}".format(max(corr)))
    # print("L'ascissa corrispondente è {} ms".format(dt[argmax(corr)]))
    time_shift = dt[argmax(corr)]

    # Qua il phase shift usando le frequenze in input
    # Secondo me però è ridondante dato che già time_shift dipende dalla frequenza in input
    # essendo calcolato a partire da corr(v, pere), in "pere" dipendenza da f in Hz
    phase_shift.append(2*math.pi*time_shift*frequencies[x])

    # Qua il phase shift usando il periodo di input della corrente, ovvero 0.5 secondi
    # la simulazione dura 500 ms
    # phase_shift.append(2 * math.pi * time_shift * 1/0.5)

    # plt.plot(dt, corr/10**-8)
    # plt.title("Correlation function for {} Hz".format(frequencies[x]))
    # plot_tools.plot_voltage_and_current_traces(state_monit, current, title=" ")
    # plt.show()
    print(x)
    x += 1

plt.figure("Figura 1")
plt.ylabel("Phase Shift from -2pi to 2pi")
plt.xlabel("Frequency (Hz)")
plt.plot(frequencies, phase_shift)


"""
plt.figure("Figura 2")
plt.plot(frequencies, amplitude)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Max Volt Reached (V)")

#  Si tratta di Low-pass filter
"""

plt.show()