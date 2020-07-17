import brian2 as b2
import matplotlib.pyplot as plt
import neurodynex.exponential_integrate_fire.exp_IF as exp_IF
from neurodynex.tools import plot_tools, input_factory

"""
print("La corrente minima per avere uno spike è 0.4236")
i = 0.4236

input_current = input_factory.get_step_current(
    t_start=20, t_end=120, unit_time=b2.ms, amplitude=i * b2.namp)

state_monitor1, spike_monitor1 = exp_IF.simulate_exponential_IF_neuron(
    I_stim=input_current, simulation_time=300 * b2.ms)

# v_rheobase=-63.1*b2.mV

print("For current {} nA".format(i))
print("Number of spikes: {}\n".format(spike_monitor1.count[0]))

plt.figure("Fig1")
plot_tools.plot_voltage_and_current_traces(
    state_monitor1, input_current, title="step current", firing_threshold=exp_IF.FIRING_THRESHOLD_v_spike)
plt.show()
"""

i = 4  # change i and find the value that goes into min_amp
durations = [1,   2,    5,  10,   20,   50, 100]
min_amp = [0., 4.42, 0., 1.10, .70, .48, 0.]

t = durations[i]
I_amp = min_amp[i]*b2.namp
title_txt = "I_amp={}, t={}".format(I_amp, t*b2.ms)

input_current = input_factory.get_step_current(t_start=10, t_end=10+t-1, unit_time=b2.ms, amplitude=I_amp)

state_monitor, spike_monitor = exp_IF.simulate_exponential_IF_neuron(I_stim=input_current, simulation_time=(t+20)*b2.ms)

plt.figure(1)
plot_tools.plot_voltage_and_current_traces(state_monitor, input_current,
                                           title=title_txt, firing_threshold=exp_IF.FIRING_THRESHOLD_v_spike,
                                           legend_location=2)
print("nr of spikes: {}".format(spike_monitor.count[0]))

plt.figure(2)
plt.plot(durations, min_amp)
plt.title("Strength-Duration curve")
plt.xlabel("t [ms]")
plt.ylabel("min amplitude [nAmp]")
plt.show()
