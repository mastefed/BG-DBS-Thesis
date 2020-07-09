# Modeling a network of Inhibitory and Excitatory Adaptive Exponential IF neurons

from brian2 import *
import pandas as pd
import matplotlib.pyplot as plt
start_scope()

C = 281*pfarad
gl = 30*nsiemens
El = -70.6*mV
vt = - 50.4*mV
delt = 2*mV
tau = 144*ms
a = 4*nsiemens
b = 0.0805*namp
sigma = 0.6*namp*(ms**0.5)
duration = 500*ms
ninhib = 250
nexcit = 1000

# I corrente esterna
eqs = '''
dv/dt = ( - gl * (v - El) + gl * delt * exp((v - vt)/delt) - w + I + sigma*xi)/C : volt
dw/dt = ( a * (v - El) - w)/tau : amp
I : amp
'''

neuroneinhib = NeuronGroup(ninhib, eqs, threshold='v>20*mV', reset='v=El;w=w+b', method='euler')
neuroneexcit = NeuronGroup(nexcit, eqs, threshold='v>20*mV', reset='v=El;w=w+b', method='euler')

monitorinhib = StateMonitor(neuroneinhib, 'v', record=True)
monitorexcit = StateMonitor(neuroneexcit, 'v', record=True)

spikesinhib = SpikeMonitor(neuroneinhib)
spikesexcit = SpikeMonitor(neuroneexcit)

neuroneinhib.v = El
neuroneexcit.v = El
neuroneinhib.I = 0*nA

S1 = Synapses(neuroneexcit, neuroneinhib, 'h : 1', on_pre='v_post += 1.5*mV')
S1.connect(condition='abs(i-j)<4 and i!=j', p=0.8)
S2 = Synapses(neuroneinhib, neuroneexcit, 'z : 1', on_pre='v_post += -1.5*mV')
S2.connect(condition='abs(i-j)<4 and i!=j', p=0.8)
S2.delay = '2*ms'
S3 = Synapses(neuroneexcit, neuroneexcit, 'u : 1', on_pre='v_post += 1.5*mV')
S3.connect(condition='abs(i-j)<4 and i!=j', p=0.5)
S4 = Synapses(neuroneinhib, neuroneinhib, 'g : 1', on_pre='v_post += -1.5*mV')
S4.connect(condition='abs(i-j)<4 and i!=j', p=0.5)
S4.delay = '2*ms'



numspikes = []
numspikesintervals = []
corrente = []

# Dummy mi serve per registrare la corrente e creare l'array di riferimento
for l in range(10):
    dummy = rand()*3*nA
    neuroneexcit.I = dummy
    corrente.append(dummy)
#    print(dummy)
#    print(neuroneexcit.I)
    run(50 * ms)
    numspikes.append(spikesexcit.num_spikes)
    
corrente.append(0*nA)

print("Il numero totale di spikes durante la simulazione è:")
print(numspikes[9])
print(" ")

numspikesintervals.append(numspikes[0])
for l in range(1,10):
    numspikesintervals.append(numspikes[l] - numspikes[l-1])

print("La variazione di spikes per ogni intervallo di 50 ms, in conseguenza al cambio della corrente di input in maniera randomica, invece è:")
print(numspikesintervals)
print(" ")

timeintervals = arange(50,600,50)
# print(timeintervals)
timespan = arange(0,550,50)

freqspikesinterval = []
for l in range(10):
    freqspikesinterval.append(numspikesintervals[l]/50*ms)
    
freqspikesinterval.append(0*ms)

print("Quindi la frequenza di spikes per ogni intervallo di 50 ms è:")
print(freqspikesinterval)
print(" ")

print("Le correnti utilizzate durante la simulazione sono:")
print(corrente)

"""
plt.figure("Potential Membrane")
plt.subplot(211)
for l in range(11):
    axvline(l*50, ls='--', c='b',lw=1)
plt.plot(monitorinhib.t/ms, monitorinhib.v.T/mV,'b',lw=0.7)
ylabel("V (mV) Inhibitory")

plt.subplot(212)
plt.plot(monitorexcit.t/ms, monitorexcit.v.T/mV,'g',lw=0.7)
for l in range(11):
    axvline(l*50, ls='--', c='g',lw=1)
xlabel("Time (ms)")
ylabel("V (mV) Excitatory")
"""

plt.figure("Raster plot (Excitatory)")

plt.subplot(211)
plt.plot(spikesexcit.t/ms, spikesexcit.i, '.g', ms=1.5)
for l in range(11):
    axvline(l*50, ls='--', c='g', lw=1)
plt.xticks(timespan)
ylabel("Neuron Index")

plt.subplot(212)
plt.plot(timespan, corrente/nA, 'g')
plt.xticks(timespan)
plt.grid(color='g', linestyle='--', linewidth=1)
ylabel("Input current (nA)")
xlabel("Time (ms)")

plt.figure("Raster plot (Inhibitory)")

plt.subplot(211)
plt.plot(spikesinhib.t/ms, spikesinhib.i, '.b')
for l in range(11):
    axvline(l*50, ls='--', c='b', lw=1)
plt.xticks(timespan)
ylabel("Neuron Index")

plt.subplot(212)
plt.plot(timespan, corrente/nA, 'g')
plt.xticks(timespan)
plt.grid(color='g', linestyle='--', linewidth=1)
ylabel("Input current (nA)")
xlabel("Time (ms)")


plt.figure("Firing rate against input current")
plt.plot(corrente/nA, freqspikesinterval/mhertz, 'og')
plt.grid(color='g', linestyle='--', linewidth=1)
xlabel("Input current (nA)")
ylabel("Firing rate (mHz)")

"""
plt.figure("Firing rate against time intervals")
plt.plot(timeintervals, freqspikesinterval/mhertz, 'og')
plt.xticks(timeintervals)
plt.grid(color='g', linestyle='--', linewidth=1)
xlabel("Time intervals (ms)")
ylabel("Firing rate for each time interval (mHz)")
"""

plt.show()
