# Population Parameters
neuron = {'D1': 5000, 'D2': 5000, 'FSN': 210, 'GPTA': 658, 'GPTI': 1976, 'GPI': 1508, 'STN': 776}

# Neuron Parameters
neuronparameters = {
"GPTI" : {"a" : 2.5, "b" : 70.0, "Delta_T" : 1.7, "tau_w": 20.0,
          "E_L": -55.1, "g_L": 1.0,  "C_m": 40.0,"I_e":12.0, "V_peak":15.00,
            "V_reset": -60.0, "V_th": -50.7,
            "tau_syn_ex":2.0, "tau_syn_in":4.0 ,'V_m': -55.1, 'E_in' : -65.0, 'E_ex': 0.0
            },
            
"GPTA" : {"a" : 2.5, "b" : 105.0, "Delta_T" : 2.55, "tau_w": 20.0,
          "E_L": -55.1, "g_L": 1.0,  "C_m": 60.0,"I_e":1.0, "V_peak":15.0,
            "V_reset": -60.0, "V_th": -50.7,
            "tau_syn_ex":2.0, "tau_syn_in":4.0 , 'V_m' : -55.1, 'E_in' : -65.0, 'E_ex': 0.0
            },

"GPI" : {"a" : 3.0, "b" : 200.0, "Delta_T" : 1.8, "tau_w": 20.0,
          "E_L": -55.8, "g_L": 3.0,  "C_m": 80.0,"I_e":15.0, "V_peak":20.0,
            "V_reset": -65.0, "V_th": -50.2,
            "tau_syn_ex":8.0, "tau_syn_in":2.0 , 'V_m' : -55.8, 'E_in' : -80.0, 'E_ex': 0.0
            },

"STN" : {"a" : 2.5, "b" : 70.0, "Delta_T" : 1.7, "tau_w": 20.0,
          "E_L": -80.2, "g_L": 10.0, "C_m": 60.0, "I_e":5.0,
            "V_reset": -70.0, "V_th": -64.0, "V_peak": 15.0,
            "tau_syn_ex":2.0, "tau_syn_in":4.0, 'V_m' :  -80.2, 'E_in' : -84.0, 'E_ex': 0.0
            },

"FSN" : {"V_m" : -80.0, "E_ex" : 0.0, "E_in": -76.0, "V_th": -50.0, "tau_syn_ex":2.0, "tau_syn_in":4.0,
            "C_m": 80.0, "g_L": 20.0, "I_e" : 500.0,"E_L":-80.0, "V_reset":-60, "t_ref":2},

"D1" : {"V_m" : -78.2, "E_ex" : 0.0, "E_in": -74.0, "V_th": -29.7, "tau_syn_ex":2.0, "tau_syn_in":4.0,
            "C_m": 200.0, "g_L": 12.5, "I_e":350.0,"E_L":-78.2, "V_reset":-60, "t_ref":2},

"D2" : {"V_m" : -80.0, "E_ex" : 0.0, "E_in": -74.0, "V_th": -29.7, "tau_syn_ex":2.0, "tau_syn_in":4.0,
            "C_m": 200.0, "g_L": 12.5, "I_e": 350.0,"E_L":-80.0, "V_reset":-60, "t_ref":2}
}

# Poisson noise
poissoninput = {
  'FSN' : {'num' : 210, 'rate' : 1000., 'weight' : 1.45, 'delay' : 1.}, # 1000 400
  'D1' : {'num' : 5000, 'rate' : 2930., 'weight' : 1.45, 'delay' : 1.}, # 2930 2390 
  'D2' : {'num' : 5000, 'rate' : 2560., 'weight' : 1.45, 'delay' : 1.}, # 2560 2610
  'STN' : {'num' : 776, 'rate' : 1690., 'weight' : 1.15, 'delay' : 1.}, # 1690
  'GPTI' : {'num' : 1976, 'rate' : 1650., 'weight' : 1.25, 'delay' : 1.}, # 1650
  'GPTA' : {'num' : 658, 'rate' : 330., 'weight' : 0.6, 'delay' : 1.}, # 330
  'GPI' : {'num' : 1508, 'rate' : 1250., 'weight' : 3.45, 'delay' : 1.} # 1250
}

# Static syn parameters TARGET-SOURCES
staticsyn = {   
                'D1' : {
                        'D1' : {'weight': -0.075, 'delay': 1.7}, 
                        'D2': {'weight': -0.150, 'delay': 1.7}, 
                        'FSN': {'weight': -1.2, 'delay': 1.7}, 
                        'GPTA': {'weight': -0.02, 'delay': 7.0}
                        }, 

                'D2' : {
                        'D1': {'weight': -0.150, 'delay': 1.7}, 
                        'D2': {'weight': -0.044, 'delay': 1.7}, 
                        'FSN': {'weight': -1.2, 'delay': 1.7}, 
                        'GPTA': {'weight': -0.4, 'delay': 7.0}
                        },

                "FSN" : { 
                        'FSN': {'weight': -0.5, 'delay': 1.7}, 
                        'GPTA': {'weight': -0.25, 'delay': 7.0}, 
                        'GPTI': {'weight': -1.0, 'delay': 7.0}
                        },

                "GPTA" : { 
                        'GPTA': {'weight': -0.07, 'delay': 1.0}, 
                        'GPTI': {'weight': -0.12, 'delay': 1.0}, 
                        'STN': {'weight': 0.06, 'delay': 2.0}
                        },

                "GPTI" : { 
                        'D2': {'weight': -0.6, 'delay': 7.0}, 
                        'GPTA': {'weight': -0.9, 'delay': 1.0}, 
                        'GPTI': {'weight': -1.1, 'delay': 1.0}, 
                        'STN': {'weight': 0.37, 'delay': 10.0}
                        },

                "STN" : { 
                        'GPTI': {'weight': -0.62, 'delay': 10.0}
                        },

                "GPI" :  {
                        'D1': {'weight': -1.0, 'delay': 7.0}, 
                        'GPTI': {'weight': -20.0, 'delay': 3.0}, 
                        'STN': {'weight': 0.45, 'delay': 4.5}
                        }
            }