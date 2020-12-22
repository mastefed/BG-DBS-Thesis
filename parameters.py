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
  'FSN' : {'rate' : 1000., 'weight' : 1.45, 'delay' : 1.},
  'D1' : {'rate' : 2930., 'weight' : 1.45, 'delay' : 1.},
  'D2' : {'rate' : 2560., 'weight' : 1.45, 'delay' : 1.},
  'STN' : {'rate' : 1690., 'weight' : 1.15, 'delay' : 1.},
  'GPTI' : {'rate' : 1650., 'weight' : 1.25, 'delay' : 1.},
  'GPTA' : {'rate' : 330., 'weight' : 0.6, 'delay' : 1.},
  'GPI' : {'rate' : 1250., 'weight' : 3.45, 'delay' : 1.}
}

# Static syn parameters TARGET-SOURCE
staticsyn = {   
                'D1' : {
                        'D1' : {'weight': -0.075, 'delay': 1.7, 'prob': 0.1456}, 
                        'D2': {'weight': -0.150, 'delay': 1.7, 'prob': 0.1568}, 
                        'FSN': {'weight': -1.2, 'delay': 1.7, 'prob': 0.0064}, 
                        'GPTA': {'weight': -0.02, 'delay': 7.0, 'prob': 0.004}
                        }, 

                'D2' : {
                        'D1': {'weight': -0.150, 'delay': 1.7, 'prob': 0.0336}, 
                        'D2': {'weight': -0.044, 'delay': 1.7, 'prob': 0.2016}, 
                        'FSN': {'weight': -1.2, 'delay': 1.7, 'prob': 0.0044}, 
                        'GPTA': {'weight': -0.4, 'delay': 7.0, 'prob': 0.0040}
                        },

                "FSN" : { 
                        'FSN': {'weight': -0.5, 'delay': 1.7, 'prob': 0.0952}, 
                        'GPTA': {'weight': -0.25, 'delay': 7.0, 'prob': 0.0952}, 
                        'GPTI': {'weight': -1.0, 'delay': 7.0, 'prob': 0.0952}
                        },

                "GPTA" : { 
                        'GPTA': {'weight': -0.07, 'delay': 1.0, 'prob': 0.0152}, 
                        'GPTI': {'weight': -0.12, 'delay': 1.0, 'prob': 0.0760}, 
                        'STN': {'weight': 0.06, 'delay': 2.0, 'prob': 0.0912}
                        },

                "GPTI" : { 
                        'D2': {'weight': -0.6, 'delay': 7.0, 'prob': 0.5061}, 
                        'GPTA': {'weight': -0.9, 'delay': 1.0, 'prob': 0.0051}, 
                        'GPTI': {'weight': -1.1, 'delay': 1.0, 'prob': 0.0253}, 
                        'STN': {'weight': 0.37, 'delay': 10.0, 'prob': 0.0304}
                        },

                "STN" : { 
                        'GPTI': {'weight': -0.62, 'delay': 10.0, 'prob': 0.0773}
                        },

                "GPI" :  {
                        'D1': {'weight': -1.0, 'delay': 7.0, 'prob': 0.6631}, 
                        'GPTI': {'weight': -20.0, 'delay': 3.0, 'prob': 0.0424}, 
                        'STN': {'weight': 0.45, 'delay': 4.5, 'prob': 0.0398}
                        }
            }