# Population Parameters
neuron = {'D1': 5000, 'D2': 5000, 'FSN': 210, 'GPTA': 658, 'GPTI': 1976, 'GPI': 1508, 'STN': 776}

# Neuron Parameters
neuronparameters = {
"GPTI" : {"a" : 2.5, "b" : 70.0, "Delta_T" : 1.7, "tau_w": 20.0,
          "E_L": -55.1, "g_L": 1.0,  "C_m": 40.0,"I_e":0.0, "V_peak":15.00,
            "V_reset": -60.0, "V_th": -50.7,
            "tau_syn_ex":2.0, "tau_syn_in":4.0 ,'V_m': -55.1, 'E_in' : -65.0, 'E_ex': 0.0
            },
            
"GPTA" : {"a" : 2.5, "b" : 105.0, "Delta_T" : 2.55, "tau_w": 20.0,
          "E_L": -55.1, "g_L": 1.0,  "C_m": 60.0,"I_e":0.0, "V_peak":15.0,
            "V_reset": -60.0, "V_th": -50.7,
            "tau_syn_ex":2.0, "tau_syn_in":4.0 , 'V_m' : -55.1, 'E_in' : -65.0, 'E_ex': 0.0
            },

"GPI" : {"a" : 3.0, "b" : 200.0, "Delta_T" : 1.8, "tau_w": 20.0,
          "E_L": -55.8, "g_L": 3.0,  "C_m": 80.0,"I_e":0.0, "V_peak":20.0,
            "V_reset": -65.0, "V_th": -50.2,
            "tau_syn_ex":8.0, "tau_syn_in":2.0 , 'V_m' : -55.8, 'E_in' : -80.0, 'E_ex': 0.0
            },

"STN" : {"a" : 2.5, "b" : 70.0, "Delta_T" : 1.7, "tau_w": 20.0,
          "E_L": -80.2, "g_L": 10.0, "C_m": 60.0, "I_e":0.0,
            "V_reset": -70.0, "V_th": -64.0, "V_peak": 15.0,
            "tau_syn_ex":2.0, "tau_syn_in":4.0, 'V_m' :  -80.2, 'E_in' : -84.0, 'E_ex': 0.0
            },

"FSN" : {"V_m" : -80.0, "E_ex" : 0.0, "E_in": -76.0, "V_th": -50.0, "tau_syn_ex":2.0, "tau_syn_in":4.0,
            "C_m": 80.0, "g_L": 20.0, "I_e" : 0.0,"E_L":-80.0, "V_reset":-60, "t_ref":2},

"D1" : {"V_m" : -78.2, "E_ex" : 0.0, "E_in": -74.0, "V_th": -29.7, "tau_syn_ex":2.0, "tau_syn_in":4.0,
            "C_m": 200.0, "g_L": 12.5, "I_e":0.0,"E_L":-78.2, "V_reset":-60, "t_ref":2},

"D2" : {"V_m" : -80.0, "E_ex" : 0.0, "E_in": -74.0, "V_th": -29.7, "tau_syn_ex":2.0, "tau_syn_in":4.0,
            "C_m": 200.0, "g_L": 12.5, "I_e": 0.0,"E_L":-80.0, "V_reset":-60, "t_ref":2}
}

# Poisson noise
poissoninput = {
  'FSN' : {'num' : 210, 'rate' : 3750., 'weight' : 1.4, 'delay' : 1.}, # 1000 850
  'D1' : {'num' : 5000, 'rate' : 7800., 'weight' : 1.4, 'delay' : 1.}, # 2930 4000
  'D2' : {'num' : 5000, 'rate' : 8020., 'weight' : 1.4, 'delay' : 1.}, # 2560 2560
  'STN' : {'num' : 776, 'rate' : 1750., 'weight' : 1.1, 'delay' : 1.}, # 1690 1730
  'GPTI' : {'num' : 1976, 'rate' : 2200., 'weight' : 1.2, 'delay' : 1.}, # 1650 1800
  'GPTA' : {'num' : 658, 'rate' : 900., 'weight' : 0.6, 'delay' : 1.}, # 330 900
  'GPI' : {'num' : 1508, 'rate' : 1240., 'weight' : 3.4, 'delay' : 1.} # 1250 1440
}

# Static syn parameters TARGET-SOURCES
staticsyn = {   
                'D1' : {
                        'D1' : {'weight': .075, 'delay': 1.7, 'degree': 728}, 
                        'D2': {'weight': .150, 'delay': 1.7, 'degree': 784}, 
                        'FSN': {'weight': 1.2, 'delay': 1.7, 'degree': 32}, 
                        'GPTA': {'weight': .02, 'delay': 7., 'degree': 20}
                        }, 

                'D2' : {
                        'D1': {'weight': .150, 'delay': 1.7, 'degree': 784}, 
                        'D2': {'weight': .044, 'delay': 1.7, 'degree': 1008}, 
                        'FSN': {'weight': .2, 'delay': 1.7, 'degree': 22}, 
                        'GPTA': {'weight': .4, 'delay': 7., 'degree': 20}
                        },

                "FSN" : { 
                        'D1': {'weight': 1., 'delay': 1., 'degree': 32},
                        'D2': {'weight': 1., 'delay': 1., 'degree': 22},
                        'FSN': {'weight': .5, 'delay': 1.7, 'degree': 20}, 
                        'GPTA': {'weight': .25, 'delay': 7., 'degree': 20}, 
                        'GPTI': {'weight': 1.0, 'delay': 7., 'degree': 20}
                        },

                "GPTA" : {
                        'FSN': {'weight': 2., 'delay': 1., 'degree': 20}, 
                        'GPTA': {'weight': .07, 'delay': 1., 'degree': 10}, 
                        'GPTI': {'weight': .12, 'delay': 1., 'degree': 50}, 
                        'STN': {'weight': .06, 'delay': 2., 'degree': 60}
                        },

                "GPTI" : { 
                        'D2': {'weight': .6, 'delay': 7.0, 'degree': 1000},
                        'FSN': {'weight': 1., 'delay': 1., 'degree': 20}, 
                        'GPTA': {'weight': .9, 'delay': 1., 'degree': 10}, 
                        'GPTI': {'weight': 1.1, 'delay': 1., 'degree': 50}, 
                        'STN': {'weight': .37, 'delay': 10., 'degree': 60}
                        },

                "STN" : { 
                        'GPTI': {'weight': .62, 'delay': 10., 'degree': 60}
                        },

                "GPI" :  {
                        'D1': {'weight': 1., 'delay': 7., 'degree': 1000}, 
                        'GPTI': {'weight': 20., 'delay': 3., 'degree': 64}, 
                        'STN': {'weight': .45, 'delay': 4.5, 'degree': 60}
                        }
            }
