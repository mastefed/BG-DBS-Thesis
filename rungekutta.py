import numpy as np
import matplotlib.pyplot as plt

print('Questo codice implementa un algoritmo Runge-Kutta di ordine 4')
#Definisco la mia funzione iniziale
def f(x, t):
    return (1/(x**3))*(np.exp(-t))+(np.cos(t))*(np.sin(x))
#Definisco le condizioni iniziali!
x0 = 1
t0 = 0.1
#Definisco i parametri del mio algoritmo!
h = 0.05
def k1(x, t):
    return h*f(x,t)
def k2(x, t):
    return h*f(x + k1(x,t)/2,t + h/2)
def k3(x, t):
    return h*f(x + k2(x,t)/2, t + h/2)
def k4(x, t):
    return h*f(x + k3(x,t),t+h)

t = [t0]
x = [x0]
for j in range(100):
    t.append(t[j] + h)
    x.append(x[j] + (1/6)*( k1(x[j],t[j]) + 2 * k2(x[j],t[j]) + 2*k3(x[j],t[j]) + k4(x[j],t[j])))
plt.plot(t,x)
plt.show()