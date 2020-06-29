# In the following tutorial how to simulate neuron groups changing some parameters during the simulation

from brian2 import *

start_scope ()


"""
# Parameters
num_inputs = 100
input_rate = 10*Hz
weight = 0.1

# Range of time constants
tau_range = linspace(1, 10, 30)*ms     # linear space of 30 elements from 1 to 10
# Use this list to store output rates
output_rates = []
# Iterate over range of time constants
for tau in tau_range:
    # Construct the network each time
    P = PoissonGroup(num_inputs, rates=input_rate)    # input neurons are Poisson neurons!
    eqs = '''
    dv/dt = -v/tau : 1
    '''
    G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='exact')  # these neurons are modelled by eqs
    S = Synapses(P, G, on_pre='v += weight')    # simple synapse from P to G
    S.connect()
    M = SpikeMonitor(G)
    # Run it and store the output firing rate in the list
    run(1*second)
    output_rates.append(M.num_spikes/second)
    
    What is the problem with this code? That every time I change the value of tau it has to run again the
    simulation, this build up some time and is absolutely non optimized, instead we can do something else:
"""

# Parameters
num_inputs = 100
input_rate = 10*Hz
weight = 0.1

# Range of time constant
tau_range = linspace(1, 10, 30)*ms   # linear space of 30 elements from 1 to 10 evenly spaced
output_rates = []

# Construct the network just once
P = PoissonGroup(num_inputs, rates=input_rate)
eqs = '''
dv/dt = -v/tau : 1
'''
G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='exact')
S = Synapses(P, G, on_pre='v += weight')
S.connect()
M = SpikeMonitor(G)
# Store the current state of the network
store()


for tau in tau_range:
    # Restore the original state of the network and simulate it with a different time constant!
    restore()
    # Run it with the new value of tau
    run(1*second)
    output_rates.append(M.num_spikes/second)

# And plot it
plt.figure("Results")
plt.plot(tau_range/ms, output_rates)
xlabel(r'$\tau$ (ms)')
ylabel('Firing rate (sp/s)')
plt.show()

"""
Running the Poisson group each time makes the firing rate raise not in a monotonically way!
Also, if you run the simulation multiple times the curve will be always different, that's because, again,
we're running the Poisson group each time!

On the brian2 documentation there's also a code to simulate what we did but running the poisson process
just one time and then storing the data it produces.
"""
