# Modeling an adaptive integrate and fire neuron

from brian2 import *
start_scope()

# Parameters
C = 281*pfarad
gl = 30*nsiemens
El = -70.6*mV
vt = - 50.4*mV
delt = 2*mV
tau = 144*ms
a = 4*nsiemens
b = 0.0805*namp



eqs = '''
dv/dt = ( - gl * (v - El) + gl * delt * exp((v - vt)/delt) - w + I)/C : volt
dw/dt = ( a * (v - El) - w)/tau : amp
I : amp
'''

neurone = NeuronGroup(1, eqs, threshold='v>20*mV', reset='v=El;w=w+b', method='exponential_euler')
monitor = StateMonitor(neurone, 'v', record=True)

neurone.v = rand()*mV
neurone.I = 50*nA

run(30*ms)

plt.figure("Wow")
plt.plot(monitor.t/ms, monitor.v.T/mV)
xlabel("Tempo in ms")
ylabel("Potenziale in mV")
plt.show()