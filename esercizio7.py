import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np
from neurodynex.phase_plane_analysis import fitzhugh_nagumo

# Jacobiano per un sistema Fitzhug-Nagumo
def jacob_fn(u,eps):
    return [[1-3*u**2,-1],[eps,-0.5*eps]]

"""
fitzhugh_nagumo.plot_flow()

fixed_point = fitzhugh_nagumo.get_fixed_point()
print("fixed_point: {}".format(fixed_point))

plt.figure()
trajectory = fitzhugh_nagumo.get_trajectory()
plt.plot(trajectory[0], trajectory[1])
plt.show()
"""

I = float(input("Che valore della costante I desideri?\n"))
print("\n")

x = np.arange(-1.5,1.5,0.01)
y1 = x*(1-x**2)+I
y2 = 2*x+2

u1, w1 = fitzhugh_nagumo.get_fixed_point(I)
print(u1)
print(w1)
print("\n")

eps = 0.1
J = jacob_fn(u1,eps)
eig = np.linalg.eigvals(J)

print("La matrice Jacobiana è:")
print(J[0])
print(J[1])
print("\n")
print("Gli autovalori della matrice jacobiana sono:")
print(eig)
print("\n")

u0 = 0
w0 = 0
t, u, w = fitzhugh_nagumo.get_trajectory(u0, w0, I)


plt.plot(u,w)
plt.plot(x,y1) # Nullcline 1
plt.plot(x,y2) # Nullcline 2
fitzhugh_nagumo.plot_flow()
plt.xlabel("u")
plt.ylabel("w")
plt.show()
