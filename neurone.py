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
sigma = 0.6*namp*(ms**0.5)

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


neuroneinhib.v = El
neuroneexcit.v = El

neuroneinhib.I = 0*nA

S1 = Synapses(neuroneexcit, neuroneinhib, 'h : 1', on_pre='v_post += 20*mV')
S1.connect(i=0,j=0)
S2 = Synapses(neuroneinhib, neuroneexcit, 'z : 1', on_pre='v_post += -20*mV')
S2.connect(i=0,j=0)
S2.delay = '2*ms'

neuroneexcit.run_regularly('I = rand()*3*nA', dt=10*ms)
run(130*ms)

plt.figure("Inhib and excit")
plt.subplot(211)
plt.plot(monitorinhib.t/ms, monitorinhib.v.T/mV,'b')
ylabel("V (mV) Inhibitory")
plt.subplot(212)
plt.plot(monitorexcit.t/ms, monitorexcit.v.T/mV,'g')
xlabel("Tempo in ms")
ylabel("V (mV) Excitatory")
plt.show()