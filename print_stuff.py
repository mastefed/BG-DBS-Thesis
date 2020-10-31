"""
Plotting useful stuff down here!
"""

""" Plotting the Population Rate over time during simulation
"""
b2.plt.figure("Pop Rate")
b2.plt.title("Population firing rate for STN (green) and GPe (blue) populations ")
b2.plt.ylabel("Firing Rate (Hz)")
b2.plt.xlabel("Time (ms)")
b2.plt.plot(populationSTNRB.t/b2.ms, populationSTN/b2.Hz, 'g')
b2.plt.plot(populationGPeB.t/b2.ms, populationGPe/b2.Hz, 'b')



""" Plotting Excitatory and Inhibitory currents in my loop
"""
b2.plt.figure("Exci-Inhi")
b2.plt.title("Excitatory (green) and Inhibitory (red) Currents in the STN-GPe loop")
b2.plt.ylabel("Currents (pA)")
b2.plt.xlabel("Time (ms)")
plotExciCurrent = b2.plt.plot(statemonitorGPeB.t/b2.ms,mean_I_exci/b2.pamp, 'g')
plotInhiCurrent = b2.plt.plot(statemonitorGPeB.t/b2.ms,mean_I_inhi/b2.pamp, 'r')

b2.plt.figure("Currents in STN and GPe")
b2.plt.title("Currents arriving at STN (green) and GPe (blue)")
b2.plt.ylabel("Currents (pA)")
b2.plt.xlabel("Time (ms)")
plotExciCurrent = b2.plt.plot(statemonitorGPeB.t/b2.ms,tot_curr_to_STN/b2.pamp, 'g')
plotInhiCurrent = b2.plt.plot(statemonitorGPeB.t/b2.ms,tot_curr_to_GPe/b2.pamp, 'b')



""" Plotting STN stuff
"""
b2.plt.figure("Membrane potential STN")
b2.plt.title("Membrane potential of one neuron (red = STN RB) (green = STN LLRS) (blue = STN NR)")
b2.plt.ylabel("Neuron membrane voltage")
b2.plt.xlabel("Time (ms)")
plotSSTNNR = b2.plt.plot(statemonitorSTNNR.t/b2.ms, statemonitorSTNNR.v[0]/b2.mV, 'b')
plotSSTNLLRS = b2.plt.plot(statemonitorSTNLLRS.t/b2.ms, statemonitorSTNLLRS.v[0]/b2.mV, 'g')
plotSSTNRB = b2.plt.plot(statemonitorSTNRB.t/b2.ms, statemonitorSTNRB.v[0]/b2.mV, 'r')


b2.plt.figure("Spikes STN")
b2.plt.title("Raster plot (red = STN RB) (green = STN LLRS) (blue = STN NR)")
b2.plt.ylabel("Neuron Index")
b2.plt.xlabel("Time (ms)")
b2.plt.ylim((0,45))
plotMSTNRB = b2.plt.plot(spikemonitorSTNRB.t/b2.ms, spikemonitorSTNRB.i, 'r.',ms='2')
plotMSTNLLRS = b2.plt.plot(spikemonitorSTNLLRS.t/b2.ms, spikemonitorSTNLLRS.i, 'g.',ms='2')
plotMSTNNR = b2.plt.plot(spikemonitorSTNNR.t/b2.ms, spikemonitorSTNNR.i, 'b.',ms='2')



""" Plotting GPe stuff
"""
b2.plt.figure("Membrane potential GPe")
b2.plt.title("Membrane potential of one neuron (red = GPe A) (green = GPe B) (blue = GPe C)")
b2.plt.ylabel("Neuron membrane voltage")
b2.plt.xlabel("Time (ms)")
plotSGPeA = b2.plt.plot(statemonitorGPeA.t/b2.ms, statemonitorGPeA.v[0]/b2.mV, 'r')
plotSGPeB = b2.plt.plot(statemonitorGPeB.t/b2.ms, statemonitorGPeB.v[0]/b2.mV, 'g')
plotSGPeC = b2.plt.plot(statemonitorGPeC.t/b2.ms, statemonitorGPeC.v[0]/b2.mV, 'b')


b2.plt.figure("Spikes GPe")
b2.plt.title("Raster plot (red = GPe A) (green = GPe B) (blue = GPe C)")
b2.plt.ylabel("Neuron Index")
b2.plt.xlabel("Time (ms)")
b2.plt.ylim((0,153))
plotMGPeA = b2.plt.plot(spikemonitorGPeA.t/b2.ms, spikemonitorGPeA.i, 'r.',ms='2')
plotMGPeB = b2.plt.plot(spikemonitorGPeB.t/b2.ms, spikemonitorGPeB.i, 'g.',ms='2')
plotMGPeC = b2.plt.plot(spikemonitorGPeC.t/b2.ms, spikemonitorGPeC.i, 'b.',ms='2')

