# Modeling an adaptive integrate and fire neuron

from brian2 import *
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

# I corrente esterna
eqs = '''
dv/dt = ( - gl * (v - El) + gl * delt * exp((v - vt)/delt) - w + I + sigma*xi)/C : volt
dw/dt = ( a * (v - El) - w)/tau : amp
I : amp
'''

neuroneinhib = NeuronGroup(1, eqs, threshold='v>20*mV', reset='v=El;w=w+b', method='euler')
neuroneexcit = NeuronGroup(1, eqs, threshold='v>20*mV', reset='v=El;w=w+b', method='euler')

monitorinhib = StateMonitor(neuroneinhib, 'v', record=True)
monitorexcit = StateMonitor(neuroneexcit, 'v', record=True)

spikesinhib = SpikeMonitor(neuroneinhib)
spikesexcit = SpikeMonitor(neuroneexcit)

neuroneinhib.v = El
neuroneexcit.v = El
neuroneinhib.I = 0*nA

S1 = Synapses(neuroneexcit, neuroneinhib, 'h : 1', on_pre='v_post += 20*mV')
S1.connect(i=0,j=0)
S2 = Synapses(neuroneinhib, neuroneexcit, 'z : 1', on_pre='v_post += -20*mV')
S2.connect(i=0,j=0)
S2.delay = '2*ms'

numspikes = []
numspikesintervals = []
corrente = []

for l in range(10):
    dummy = rand()*3*nA
    neuroneexcit.I = dummy
    corrente.append(dummy)
#    print(dummy)
#    print(neuroneexcit.I)
    run(50 * ms)
    numspikes.append(spikesexcit.num_spikes)

print("Il numero totale di spikes durante la simulazione è:")
print(numspikes[9])
print(" ")

numspikesintervals.append(numspikes[0])
for l in range(1,10):
    numspikesintervals.append(numspikes[l] - numspikes[l-1])

print("La variazione di spikes per ogni intervallo di 50 ms, in conseguenza al cambio della corrente di input in maniera randomica, invece è:")
print(numspikesintervals)
print(" ")

timeintervals = arange(50,550,50)
# print(timeintervals)

freqspikesinterval = []
for l in range(10):
    freqspikesinterval.append(numspikesintervals[l]/50*ms)

print("Quindi la frequenza di spikes per ogni intervallo di 50 ms è:")
print(freqspikesinterval)
print(" ")

print("Le correnti utilizzate durante la simulazione sono:")
print(corrente)

plt.figure("Potential Membrane")
plt.subplot(211)
for l in range(11):
    axvline(l*50, ls='--', c='b',lw=1)
plt.plot(monitorinhib.t/ms, monitorinhib.v.T/mV,'b')
ylabel("V (mV) Inhibitory")

plt.subplot(212)
plt.plot(monitorexcit.t/ms, monitorexcit.v.T/mV,'g')
for l in range(11):
    axvline(l*50, ls='--', c='g',lw=1)
xlabel("Time (ms)")
ylabel("V (mV) Excitatory")

plt.figure("Firing rate against input current")
plt.plot(corrente/nA, freqspikesinterval/mhertz, 'og')
plt.grid(color='g', linestyle='--', linewidth=1)
xlabel("Input current (nA)")
ylabel("Firing rate (mHz)")

plt.figure("Firing rate against time intervals")
plt.plot(timeintervals, freqspikesinterval/mhertz, 'og')
plt.xticks(timeintervals)
for l in range(1,11):
    axvline(l*50, ls='--', c='g',lw=1)
xlabel("Time intervals (ms)")
ylabel("Firing rate for each time interval (mHz)")
plt.show()
