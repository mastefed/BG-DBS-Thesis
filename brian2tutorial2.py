# In this tutorial we see hot to link neurons via artificial synapses and how many ways to do it there are


from brian2 import *

start_scope()

eqs = '''
dv/dt = (I-v)/tau : 1 (unless refractory)
I : 1
tau : second
'''

G = NeuronGroup(3, eqs, threshold='v>1', reset='v = 0', refractory=5*ms, method='exact')
G.I = [2, 0, 0]
G.tau = [10, 100, 100]*ms

# This creates the synapse specifying the source and the receiver and the weigh of the link
# S.connect specifies the connection typology which can be exact for very few neurons or probabilistic
# for much more neurons, like 15+

S = Synapses(G, G, 'w : 1', on_pre='v_post += w')
S.connect(i=0, j=[1,2])
S.w = 'j*0.2'
S.delay = 'j*2*ms'


# S.connect(condition='i!=j', p=0.2)
# This connects neurons with a probability of 0.2

# S.connect(condition='abs(i-j)<4 and i!=j')
# This connects neurons specifying the condition that only the neighbours shall be connected



M = StateMonitor(G, 'v', record=True)

run(100*ms)

f = plt.figure(1)
plt.plot(M.t/ms, M.v[0], label='Neuron 0')
plt.plot(M.t/ms, M.v[1], label='Neuron 1')
plt.plot(M.t/ms, M.v[2], label='Neuron 2')
xlabel('Time (ms)')
ylabel('v')
legend();
plt.show()

