leakyif = """
dV/dt = (-g_L*(V-E_L) - g_e*(V-E_ex) - g_i*(V-E_in) + I_e)/C_m : volt

dg_e/dt = (h_e-g_e)/tau_syn_ex : siemens
dh_e/dt = -h_e/tau_syn_ex : siemens

dg_i/dt = (h_i-g_i)/tau_syn_in : siemens
dh_i/dt = -h_i/tau_syn_in : siemens

C_m : farad
g_L : siemens
E_L : volt
I_e : amp
E_ex : volt
E_in : volt
tau_syn_ex : second
tau_syn_in : second
"""

adexif = """
dV/dt = (-g_L*(V-E_L) + g_L*Delta_T*exp((V-V_th)/Delta_T) - g_e*(V-E_ex) - g_i*(V-E_in) - w + I_e)/C_m : volt
dw/dt = (1/tau_w)*(a*(V-E_L)-w) : amp

dg_e/dt = -g_e/tau_syn_ex : siemens
dg_i/dt = -g_i/tau_syn_in : siemens

C_m : farad
g_L : siemens
E_L : volt
I_e : amp
Delta_T : volt
E_ex : volt
E_in : volt
a : siemens
tau_w : second
V_th : volt
tau_syn_ex : second
tau_syn_in : second
"""