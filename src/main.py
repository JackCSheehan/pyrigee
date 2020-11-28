'''
Example usage of Pyrigee
'''

from Pyrigee import *

body = EARTH

craft = SPACE_SHUTTLE

orbit2 = Orbit(10000, 100, 25)
orbit1 = Orbit(200, 200, 0)

man = Maneuver(orbit2, "lightseagreen")

p = OrbitPlotter(body)

p.plot(orbit1, craft)

p.visualize()

