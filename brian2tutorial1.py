#Questo è il codice usato nel tutorial di Brian2.0


from brian2 import *

start_scope()

N = 100
tau = 10*ms
v0_max = 1.5
duration = 1000*ms
eqs = '''
dv/dt = (v0-v)/tau : 1 (unless refractory)
v0 : 1
'''
G = NeuronGroup(N, eqs, threshold='v>1', reset='v=0', refractory=5*ms, method='exact')
G.v = 'rand()'
#M = StateMonitor(G, 'v', record=0)

S = SpikeMonitor(G)
G.v0 = 'i*v0_max/(N-1)'


#print('Before v = %s' % G.v[0])  #Occhio qua, per mostrare la variabile v devo usare G.v[0], non semplicemente v!


run(duration)


#print('After v = %s' % G.v[0])
#print('Expected value of v = %s' % (1-exp(-100*ms/tau)))

f = plt.figure(1)
plt.plot(S.t/ms, S.i, '.k')
xlabel('Time (ms)')
ylabel('Indice del neurone');

#g = plt.figure(2)
#plt.plot(M.t/ms, M.v[0])
#for t in S.t:
    #axvline(t/ms, ls='--', c='C1', lw=2)
#xlabel('Time (ms)')
#ylabel('v')

h = plt.figure(3)
plt.plot(G.v0, S.count/duration)
xlabel('v0')
ylabel('Firing rate (sp/s)')

plt.show()

