import brian2 as b2
import matplotlib.pyplot as plt
from neurodynex.adex_model import AdEx
from neurodynex.tools import plot_tools, input_factory

"""
MEMBRANE_TIME_SCALE_tau_m = 5 * b2.ms
MEMBRANE_RESISTANCE_R = 500*b2.Mohm
V_REST = -70.0 * b2.mV
V_RESET = -51.0 * b2.mV
RHEOBASE_THRESHOLD_v_rh = -50.0 * b2.mV
SHARPNESS_delta_T = 2.0 * b2.mV
ADAPTATION_VOLTAGE_COUPLING_a = 0.5 * b2.nS
ADAPTATION_TIME_CONSTANT_tau_w = 100.0 * b2.ms
SPIKE_TRIGGERED_ADAPTATION_INCREMENT_b = 7.0 * b2.pA
"""

current = input_factory.get_step_current(10, 250, 1. * b2.ms, 65.0 * b2.pA)
# Variare l'adaptation voltage coupling influisce sul numero di spikes
# Il bursting si ottiene cambiando il valore del reset del potenziale, ovviamente
# in tal modo ti posizioni in un altro punto dello spazio delle fasi
# "a" cambia anche la posizione dei punti di equilibrio a seconda della positività o negatività

state_monitor, spike_monitor = AdEx.simulate_AdEx_neuron(I_stim=current, simulation_time=400 * b2.ms,
                                                         a=-0.5*b2.nS,
                                                         v_reset=-46*b2.mV)

plt.figure(1)
plot_tools.plot_voltage_and_current_traces(state_monitor, current)
print("nr of spikes: {}".format(spike_monitor.count[0]))
plt.figure(2)
AdEx.plot_adex_state(state_monitor)
plt.show()