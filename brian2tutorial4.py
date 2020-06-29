"""
In this tutorial (following the third one) we'll change dynamically the amplitude of the current injecetd in a HH
neuron!
"""


from brian2 import *

start_scope()

# Parameters
area = 20000*umetre**2
# Cm = 1*ufarad*cm**-2 * area
gl = 5e-5*siemens*cm**-2 * area
El = -65*mV
EK = -90*mV
ENa = 50*mV
g_na = 100*msiemens*cm**-2 * area
g_kd = 30*msiemens*cm**-2 * area
VT = -63*mV
N = 3

eqs_HH = '''
dv/dt = (gl*(El-v) - g_na*(m*m*m)*h*(v-ENa) - g_kd*(n*n*n*n)*(v-EK) + I)/C : volt
dm/dt = 0.32*(mV**-1)*(13.*mV-v+VT)/
    (exp((13.*mV-v+VT)/(4.*mV))-1.)/ms*(1-m)-0.28*(mV**-1)*(v-VT-40.*mV)/
    (exp((v-VT-40.*mV)/(5.*mV))-1.)/ms*m : 1
dn/dt = 0.032*(mV**-1)*(15.*mV-v+VT)/
    (exp((15.*mV-v+VT)/(5.*mV))-1.)/ms*(1.-n)-.5*exp((10.*mV-v+VT)/(40.*mV))/ms*n : 1
dh/dt = 0.128*exp((17.*mV-v+VT)/(18.*mV))/ms*(1.-h)-4./(1+exp((40.*mV-v+VT)/(5.*mV)))/ms*h : 1
I : amp (shared)
C : farad
'''

# To understand the reason to put that value for refractoriness check the documentation at
# https://brian2.readthedocs.io/en/stable/user/refractoriness.html
group = NeuronGroup(N, eqs_HH,
                    threshold='v > -40*mV',
                    refractory='v > -40*mV',
                    method='exponential_euler')

# Forcing the potential to be equal to the value of the leak reversal potential
group.v = El
group.C = array([0.8, 1, 1.2])*ufarad*cm**-2*area

statemon = StateMonitor(group, 'v', record=True)
spikemon = SpikeMonitor(group, variables='v')

'''
This is not the most optimized way to run the simulation, instead we can use the
run_regularly function associated with the NeuronGroup (group) specifying the 
string which states what changes and the interval time after which
the current shall change

plt.figure(figsize=(9, 4))

# This makes the current injected change five times using a rand function, then run the simulation for 10 ms
for l in range(5):
    group.I = rand()*50*nA
    run(10*ms)
    # Adding one vertical line whenever each 10 ms simulation is ran
    axvline(l*10, ls='--', c='k')
'''

# we replace the loop with a run_regularly in which the current changes five times using a rand() function
group.run_regularly('I = rand()*50*nA', dt=10*ms)
run(50*ms)
plt.figure(figsize=(9, 4))

# we keep the loop just to draw the vertical lines
for l in range(5):
    axvline(l*10, ls='--', c='k')


# Makes sure that the starting point for the potential is highlighted
axhline(El/mV, ls='-', c='lightgray', lw=3)

plt.plot(statemon.t/ms, statemon.v.T/mV, '-')
plt.plot(spikemon.t/ms, spikemon.v/mV, 'ob')
xlabel('Time (ms)')
ylabel('v (mV)')
plt.show()

'''
If I wanna run multiple neurons I can change 1 to 3 in the NeuronGroup. What if I want to share the infected
current among the three neurons? Piece of cake: in the model description I add (shared) after I
'''