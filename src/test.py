'''spacecraft = {
    "mass": 9525
}

earth = {
    "mass": 5.972E24
}

G = 6.67E-11

def calc_grav_force(m1, m2, r):
    return G * m1 * m2 / r**2

print(calc_grav_force(spacecraft["mass"], earth["mass"], 100000))
'''

import matplotlib.pyplot as plt
import numpy as np


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# PLANET GRAPH
# Radius of sphere
r = 6.371

theta, phi = np.mgrid[0:2*np.pi:15j, 0:np.pi:15j]

x = r * np.cos(theta) * np.sin(phi)
y = r * np.sin(theta) * np.sin(phi)
z = r * np.cos(phi)

ax.plot_wireframe(x, y, z, color = "b")

# Graph data
ax.set_xlabel("1000 km")
ax.set_ylabel("1000 km")
ax.set_zlabel("1000 km")

ax.set_xlim(-r - 1.5, r + 1.5)
ax.set_ylim(-r - 1.5, r + 1.5)
ax.set_zlim(-r, r)

# ORBIT GRAPH
major_axis = r + 1
minor_axis = r + 7

theta = np.mgrid[0:2*np.pi:15j]

x = major_axis * np.cos(np.linspace(0, 2 * np.pi))
y = minor_axis * np.sin(np.linspace(0, 2 * np.pi))

ax.plot(x, y + 5, zs = 0, zdir = "z", color = "r")

plt.show()