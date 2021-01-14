import matplotlib.pyplot as plt

from brian2 import *

# Fix seed for reproducible results
seed(42)

# Vary the correlation within the group
for i, c in enumerate([0.0]):

    tau = 10*ms
    eqs = '''
    dv/dt = (1-v)/tau + h/tau : 1
    h : 1
    '''

    G = NeuronGroup(5, eqs, threshold='v>0.8', reset='v = 0', method='exact')
    S = Synapses(G,G, delay=1*ms, model='''k:1''', on_pre='h += k')
    S.connect()
    S.k = '1+rand()'
    print(S.k)
    
    # Run simulation
    duration = 1 * second
    run(duration)