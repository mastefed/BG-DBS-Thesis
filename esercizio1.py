# Primo esercizio tra quelli proposti

import brian2 as b2
import matplotlib.pyplot as plt
from neurodynex.leaky_integrate_and_fire import LIF
from neurodynex.tools import input_factory, plot_tools
from neurodynex.tools.spike_tools import *

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

current = input_factory.get_sinusoidal_current(t_start=5,
                                               t_end=45,
                                               unit_time=0.1*b2.ms,
                                               amplitude=5*b2.nA,
                                               frequency=1*b2.kHz,
                                               direct_current=2.2*b2.nA,
                                               phase_offset=0.0,
                                               append_zero=True)

(state_monit, spike_monit) = LIF.simulate_LIF_neuron(input_current=current,
                                                     simulation_time=50.*b2.ms,
                                                     v_rest=-70.*b2.mV,
                                                     v_reset=-65.*b2.mV,
                                                     firing_threshold=-50.*b2.mV,
                                                     membrane_resistance=10. * b2.Mohm,
                                                     membrane_time_scale=8. * b2.msecond,
                                                     abs_refractory_period=2. * b2.msecond)

plot_tools.plot_voltage_and_current_traces(state_monit, current, title=" ")
plt.show()
