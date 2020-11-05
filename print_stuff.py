""" Plotting useful stuff down here!
"""

""" Plotting the Population Rate over time during simulation
"""
plt.figure("Pop Rate")
plt.title("Population firing rate for STN (green) and GPe (blue) populations ")
plt.ylabel("Firing Rate (Hz)")
plt.xlabel("Time (ms)")
plt.plot(populationSTNRB.t/ms, populationSTNfr/Hz, 'g')
plt.plot(populationGPeB.t/ms, populationGPefr/Hz, 'b')

""" Plotting Excitatory and Inhibitory currents in my loop
"""
plt.figure("Exci-Inhi")
plt.title("Excitatory (green) and Inhibitory (red) Currents in the STN-GPe loop")
plt.ylabel("Currents (pA)")
plt.xlabel("Time (ms)")
plotExciCurrent = plt.plot(statemonitorGPeB.t/ms,mean_I_exci/pamp, 'g')
plotInhiCurrent = plt.plot(statemonitorGPeB.t/ms,mean_I_inhi/pamp, 'r')

plt.figure("Currents in STN and GPe")
plt.title("Currents arriving at STN (green) and GPe (blue)")
plt.ylabel("Currents (pA)")
plt.xlabel("Time (ms)")
plotExciCurrent = plt.plot(statemonitorGPeB.t/ms,tot_curr_to_STN/pamp, 'g')
plotInhiCurrent = plt.plot(statemonitorGPeB.t/ms,tot_curr_to_GPe/pamp, 'b')

""" Plotting STN stuff
"""
plt.figure("Membrane potential STN")
plt.title("Membrane potential of one neuron (red = STN RB) (green = STN LLRS) (blue = STN NR)")
plt.ylabel("Neuron membrane voltage")
plt.xlabel("Time (ms)")
plotSSTNNR = plt.plot(statemonitorSTNNR.t/ms, statemonitorSTNNR.v[0]/mV, 'b')
plotSSTNLLRS = plt.plot(statemonitorSTNLLRS.t/ms, statemonitorSTNLLRS.v[0]/mV, 'g')
plotSSTNRB = plt.plot(statemonitorSTNRB.t/ms, statemonitorSTNRB.v[0]/mV, 'r')


plt.figure("Spikes STN")
plt.title("Raster plot (red = STN RB) (green = STN LLRS) (blue = STN NR)")
plt.ylabel("Neuron Index")
plt.xlabel("Time (ms)")
plt.ylim((0,45))
plotMSTNRB = plt.plot(spikemonitorSTNRB.t/ms, spikemonitorSTNRB.i, 'r.',ms='2')
plotMSTNLLRS = plt.plot(spikemonitorSTNLLRS.t/ms, spikemonitorSTNLLRS.i, 'g.',ms='2')
plotMSTNNR = plt.plot(spikemonitorSTNNR.t/ms, spikemonitorSTNNR.i, 'b.',ms='2')

""" Plotting GPe stuff
"""
plt.figure("Membrane potential GPe")
plt.title("Membrane potential of one neuron (red = GPe A) (green = GPe B) (blue = GPe C)")
plt.ylabel("Neuron membrane voltage")
plt.xlabel("Time (ms)")
plotSGPeA = plt.plot(statemonitorGPeA.t/ms, statemonitorGPeA.v[0]/mV, 'r')
plotSGPeB = plt.plot(statemonitorGPeB.t/ms, statemonitorGPeB.v[0]/mV, 'g')
plotSGPeC = plt.plot(statemonitorGPeC.t/ms, statemonitorGPeC.v[0]/mV, 'b')


plt.figure("Spikes GPe")
plt.title("Raster plot (red = GPe A) (green = GPe B) (blue = GPe C)")
plt.ylabel("Neuron Index")
plt.xlabel("Time (ms)")
plt.ylim((0,153))
plotMGPeA = plt.plot(spikemonitorGPeA.t/ms, spikemonitorGPeA.i, 'r.',ms='2')
plotMGPeB = plt.plot(spikemonitorGPeB.t/ms, spikemonitorGPeB.i, 'g.',ms='2')
plotMGPeC = plt.plot(spikemonitorGPeC.t/ms, spikemonitorGPeC.i, 'b.',ms='2')