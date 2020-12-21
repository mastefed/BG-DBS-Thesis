import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np

from parameters import *
from equations import *
from groupsandsynapses import *

duration = 1000*b2.ms
deft = b2.defaultclock.dt
t_recorded = np.arange(int(duration/deft))*deft

b2.run(300*b2.ms)

monitorstn = b2.StateMonitor(STN, variables=['V'], record=True)
spikesstn = b2.SpikeMonitor(STN, variables=['V'])

monitorgpti = b2.StateMonitor(GPTI, variables=['V'], record=True)
spikesgpti = b2.SpikeMonitor(GPTI, variables=['V'])

monitorgpta = b2.StateMonitor(GPTA, variables=['V'], record=True)
spikesgpta = b2.SpikeMonitor(GPTA, variables=['V'])

b2.run(duration)

print(f'\nFiring rate medio STN: {np.mean(spikesstn.count/duration)} spikes/second\n')
print(f'Firing rate medio GPTI: {np.mean(spikesgpti.count/duration)} spikes/second\n')
print(f'Firing rate medio GPTA: {np.mean(spikesgpta.count/duration)} spikes/second\n')
'''
plt.figure('STN')
plt.xlabel("t [ms]")
plt.ylabel("V [mV]")
plt.plot(t_recorded/b2.ms, monitorstn.V[5]/b2.mV, label='STN')
plt.legend()

plt.figure('GPTA')
plt.xlabel("t [ms]")
plt.ylabel("V [mV]")
plt.plot(t_recorded/b2.ms, monitorgpta.V[12]/b2.mV, label='GPTA')
plt.legend()

plt.figure('GPTI')
plt.xlabel("t [ms]")
plt.ylabel("V [mV]")
plt.plot(t_recorded/b2.ms, monitorgpti.V[3]/b2.mV, label='GPTI')
plt.legend()

plt.show()
'''