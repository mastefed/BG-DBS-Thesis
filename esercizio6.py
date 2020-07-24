import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np
from neurodynex.hodgkin_huxley import HH
from neurodynex.tools import input_factory

# La corrente minima per ottenere uno spike è 2.35 mi*amp
# I_min = 2.35

# La minima corrente per ottenere un tonic firing è 6.3 mi*amp
#I_min_rep = 6.3
#corrente = input_factory.get_step_current(10, 90, b2.ms, I_min_rep *b2.uA)

# La capacità di fare uno spike non dipende solo dal modulo della corrente
# ma anche dalla forma dell'impulso, qui di seguito si crea una rampa
# di corrente che cresce man mano

b2.defaultclock.dt = 0.02*b2.ms
slow_ramp_t_end = 40

"""
In effetti, nell'impostazione di default, t_end = 60 ms, non c'è spike,
se però diminuisco il tempo della rampa di corrente, anche solo a 40 ms,
ottengo uno spike del neurone. Quello che non ottengo però è un comportamento
da tonic firing. Man mano che diminuisco il t_end della rampa, sposto verso
sinistra lo spike del neurone, chiaramente in termini della scala temporale.
Qui sotto un aumento lento della corrente fino ad un top di 12 miA
"""

slow_ramp_current = input_factory.get_ramp_current(5, slow_ramp_t_end,
    b2.ms,0.*b2.uA, 12.0*b2.uA)
state_monitor1 = HH.simulate_HH_neuron(slow_ramp_current, 90 * b2.ms)
idx_t_end = int(round(slow_ramp_t_end*b2.ms / b2.defaultclock.dt))
voltage_slow = state_monitor1.vm[0,idx_t_end]
print("voltage_slow = {} V".format(voltage_slow))

# Qui sotto invece un aumento repentino della corrente
b2.defaultclock.dt = 0.02*b2.ms
fast_ramp_t_end = 100
fast_ramp_current = input_factory.get_ramp_current(50, fast_ramp_t_end,
    0.1*b2.ms, 0.*b2.uA, 4.5*b2.uA)
state_monitor2 = HH.simulate_HH_neuron(fast_ramp_current, 40 * b2.ms)
idx_t_end = int(round(fast_ramp_t_end*0.1*b2.ms / b2.defaultclock.dt))
voltage_fast = state_monitor2.vm[0,idx_t_end]
print("voltage_fast = {} V".format(voltage_fast))

"""
Una cosa importante che cambia è lo step temporale con il quale aumenta
la corrente. Questo dipende dal parametro dopo slow/fast_ramp_t_end.
Questo fa in modo che la fast current vada da cinque a dieci msecondi.
Uno si chiede "ma perché non mettere come prima b2.ms e rapportarsi a
questa unità di misura?", misteri della fede.
"""

HH.plot_data(state_monitor1, title="Slow")
HH.plot_data(state_monitor2, title="Fast")
plt.show()
