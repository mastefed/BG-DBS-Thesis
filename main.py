import brian2 as b2

# b2.clear_cache('cython')

import matplotlib.pyplot as plt
import numpy as np
import random as ran
import os

from parameters import *
from equations import *
from groupsandsynapses import *
from test import *

ran.seed(42)

duration = 2000*b2.ms
deft = b2.defaultclock.dt
t_recorded = np.arange(int(duration/deft))*deft

b2.run(300*b2.ms)

variables_to_record = ['V']

'''
monitord1 = b2.StateMonitor(D1, variables=variables_to_record, record=True)
monitord2 = b2.StateMonitor(D2, variables=variables_to_record, record=True)
monitorfsn = b2.StateMonitor(FSN, variables=variables_to_record, record=True)
monitorstn = b2.StateMonitor(STN, variables=variables_to_record, record=True)
monitorgpti = b2.StateMonitor(GPTI, variables=variables_to_record, record=True)
monitorgpta = b2.StateMonitor(GPTA, variables=variables_to_record, record=True)
monitorgpi = b2.StateMonitor(GPI, variables=variables_to_record, record=True)
'''

spikesd1 = b2.SpikeMonitor(D1)
spikesd2 = b2.SpikeMonitor(D2)
spikesfsn = b2.SpikeMonitor(FSN)
spikesstn = b2.SpikeMonitor(STN)
spikesgpti = b2.SpikeMonitor(GPTI)
spikesgpta = b2.SpikeMonitor(GPTA)
spikesgpi = b2.SpikeMonitor(GPI)

b2.store()

c_var1 = np.arange(0., 0.1, 0.01)
c_var2 = np.arange(0.1, 1.1, 0.1)
c_var = np.concatenate((c_var1,c_var2))

# file_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'frandff.txt')
file_path = '/home/f_mastellone/frandff.txt'
text_file = open(file_path, "w")

for i, c_i in enumerate(c_var):
    b2.restore()
    c = c_i
    b2.run(duration)

    text_file.write(f"Correlation parameter: {c}\n")
    print(f"Correlation parameter: {c}\n")

    text_file.write(f'Firing rate D1: {np.mean(spikesd1.count/duration)} spikes/second\n')
    text_file.write(f'Firing rate D2: {np.mean(spikesd2.count/duration)} spikes/second\n')
    text_file.write(f'Firing rate FSN: {np.mean(spikesfsn.count/duration)} spikes/second\n')
    print(f'Firing rate D1: {np.mean(spikesd1.count/duration)} spikes/second')
    print(f'Firing rate D2: {np.mean(spikesd2.count/duration)} spikes/second')
    print(f'Firing rate FSN: {np.mean(spikesfsn.count/duration)} spikes/second\n')

    text_file.write(f'Firing rate STN: {np.mean(spikesstn.count/duration)} spikes/second\n')
    text_file.write(f'Firing rate GPTI: {np.mean(spikesgpti.count/duration)} spikes/second\n')
    text_file.write(f'Firing rate GPTA: {np.mean(spikesgpta.count/duration)} spikes/second\n')
    text_file.write(f'Firing rate GPI: {np.mean(spikesgpi.count/duration)} spikes/second\n')
    print(f'Firing rate STN: {np.mean(spikesstn.count/duration)} spikes/second')
    print(f'Firing rate GPTI: {np.mean(spikesgpti.count/duration)} spikes/second')
    print(f'Firing rate GPTA: {np.mean(spikesgpta.count/duration)} spikes/second')
    print(f'Firing rate GPI: {np.mean(spikesgpi.count/duration)} spikes/second\n')

text_file.close()

"""
plt.figure(1)
plt.title('D1')
plt.plot(spikesd1.t/b2.ms, spikesd1.i, 'o', ms=0.5)
plt.xlabel('t [ms]')
plt.ylabel('index')

plt.figure(2)
plt.title('D2')
plt.plot(spikesd2.t/b2.ms, spikesd2.i, 'o', ms=0.5)
plt.xlabel('t [ms]')
plt.ylabel('index')

plt.figure(3)
plt.title('FSN')
plt.plot(spikesfsn.t/b2.ms, spikesfsn.i, 'o', ms=0.5)
plt.xlabel('t [ms]')
plt.ylabel('index')

plt.figure(4)
plt.title('GPTA')
plt.plot(spikesgpta.t/b2.ms, spikesgpta.i, 'o', ms=0.5)
plt.xlabel('t [ms]')
plt.ylabel('index')

plt.figure(5)
plt.title('GPTI')
plt.plot(spikesgpti.t/b2.ms, spikesgpti.i, 'o', ms=0.5)
plt.xlabel('t [ms]')
plt.ylabel('index')

plt.figure(6)
plt.title('STN')
plt.plot(spikesstn.t/b2.ms, spikesstn.i, 'o', ms=0.5)
plt.xlabel('t [ms]')
plt.ylabel('index')

plt.figure(7)
plt.title('GPi')
plt.plot(spikesgpi.t/b2.ms, spikesgpi.i, 'o', ms=0.5)
plt.xlabel('t [ms]')
plt.ylabel('index')

plt.show()
"""
