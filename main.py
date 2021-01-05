import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np
import random as ran
import os

from parameters import *
from equations import *
from groupsandsynapses import *
from test import *

ran.seed(42)

duration = 1000*b2.ms
deft = b2.defaultclock.dt
t_recorded = np.arange(int(duration/deft))*deft

b2.run(300*b2.ms)

monitord1 = b2.StateMonitor(D1, variables=['V'], record=True)
spikesd1 = b2.SpikeMonitor(D1, variables=['V'])

monitord2 = b2.StateMonitor(D2, variables=['V'], record=True)
spikesd2 = b2.SpikeMonitor(D2, variables=['V'])

monitorfsn = b2.StateMonitor(FSN, variables=['V'], record=True)
spikesfsn = b2.SpikeMonitor(FSN, variables=['V'])

monitorstn = b2.StateMonitor(STN, variables=['V'], record=True)
spikesstn = b2.SpikeMonitor(STN, variables=['V'])

monitorgpti = b2.StateMonitor(GPTI, variables=['V'], record=True)
spikesgpti = b2.SpikeMonitor(GPTI, variables=['V'])

monitorgpta = b2.StateMonitor(GPTA, variables=['V'], record=True)
spikesgpta = b2.SpikeMonitor(GPTA, variables=['V'])

monitorgpi = b2.StateMonitor(GPI, variables=['V'], record=True)
spikesgpi = b2.SpikeMonitor(GPI, variables=['V'])

c_var = [0., 0.2, 0.4, 0.6, 0.8]

save_to_file = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'output.txt')
text_file = open(save_to_file, "w")

for i, c_i in enumerate(c_var):
    c = c_i
    b2.run(duration)

    text_file.write(f"\nCorrelation parameter: {c}")

    text_file.write(f'\nFiring rate D1: {np.mean(spikesd1.count/duration)} spikes/second\n')
    text_file.write(f'Firing rate D2: {np.mean(spikesd2.count/duration)} spikes/second\n')
    text_file.write(f'Firing rate FSN: {np.mean(spikesfsn.count/duration)} spikes/second\n')

    text_file.write(f'Firing rate STN: {np.mean(spikesstn.count/duration)} spikes/second\n')
    text_file.write(f'Firing rate GPTI: {np.mean(spikesgpti.count/duration)} spikes/second\n')
    text_file.write(f'Firing rate GPTA: {np.mean(spikesgpta.count/duration)} spikes/second\n')
    text_file.write(f'Firing rate GPI: {np.mean(spikesgpi.count/duration)} spikes/second\n')

    """ff_fsn = fanofactor(duration, spikesfsn, neuron['FSN'], 0*b2.ms, 2*b2.ms, 2*b2.ms)
    ff_d1 = fanofactor(duration, spikesd1, neuron['D1'], 0*b2.ms, 2*b2.ms, 2*b2.ms)
    ff_d2 = fanofactor(duration, spikesd2, neuron['D2'], 0*b2.ms, 2*b2.ms, 2*b2.ms)

    text_file.write(f"FF FSN: {ff_fsn}")
    text_file.write(f"FF D1: {ff_d1}")
    text_file.write(f"FF D2: {ff_d2}\n")"""

    syncd1 = np.sqrt(variance_time_fluctuations_v(monitord1)/variance_time_flu_v_norm(5000, monitord1))
    syncd2 = np.sqrt(variance_time_fluctuations_v(monitord2)/variance_time_flu_v_norm(5000, monitord2))
    syncfsn = np.sqrt(variance_time_fluctuations_v(monitorfsn)/variance_time_flu_v_norm(5000, monitorfsn))

    text_file.write(f"Sync FSN: {syncfsn}")
    text_file.write(f"Sync D1: {syncd1}")
    text_file.write(f"Sync D2: {syncd2}\n")

text_file.close()