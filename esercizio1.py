# Primo esercizio tra quelli proposti

import brian2 as b2
from neurodynex.leaky_integrate_and_fire import LIF
from neurodynex.tools import input_factory, plot_tools

i_min = 2.006*b2.nA

LIF.print_default_parameters()

# corrente a gradino di valore i_min (da definire)
step_current = input_factory.get_step_current(
    t_start=5, t_end=100, unit_time=b2.ms,
    amplitude=i_min)

(state_monitor, spike_monitor) = LIF.simulate_LIF_neuron(input_current=step_current, simulation_time=100*b2.ms)

plot_tools.plot_voltage_and_current_traces(
    state_monitor, step_current, title="min input", firing_threshold=LIF.FIRING_THRESHOLD)
print("nr of spikes: {}".format(spike_monitor.count[0]))
