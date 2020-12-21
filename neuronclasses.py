class neuronpopulation():
    def __init__(self, numberofneurons):
        self.numberofneurons = numberofneurons

    def leakyif(self, dict):
        self.eqs = """
        dV/dt = (1/C_m)*(-g_L*(V-E_L)+I_e) : volt

        C_m : farad
        g_L : siemens
        E_L : volt
        I_e : amp
        """

        self.t_ref = 2.*b2.ms
        self.V_th = dict['V_th']*b2.mV
        self.V_reset = dict['V_reset']*b2.mV

        self.group = b2.NeuronGroup(self.numberofneurons, self.eqs, method='exact', threshold='V>V_th', reset='V=V_reset',
        refractory=self.t_ref)

        self.group.V = dict['V_m']*b2.mV
        self.group.C_m = dict['C_m']*b2.pfarad
        self.group.g_L = dict['g_L']*b2.nsiemens
        self.group.I_e = dict['I_e']*b2.pamp
        self.group.E_L = dict['E_L']*b2.mV
        
        return self.group

    def record(self):
        self.flowmonitor = b2.StateMonitor(self.group, ['V'], record=True)
        return self.flowmonitor

    def positivepulse(self, pulse):
        self.group.I_e += pulse
        return self.group.I_e

    def printcurrent(self):
        print(self.group.I_e)


from parameters import neuron, neuronparameters
import brian2 as b2

fsn = neuronpopulation(neuron['FSN'])
fsn.leakyif(neuronparameters['FSN'])
fsn.printcurrent()

fsn.positivepulse(1000*b2.pamp)

fsn.printcurrent()

fsn.record()

b2.run(1000*b2.ms)

print(fsn.flowmonitor.V)