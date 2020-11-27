'''
Example usage of Pyrigee
'''

from Pyrigee import *

body = EARTH

craft = SPACE_SHUTTLE

orbit1 = Orbit(100, 100, 0)
orbit2 = Orbit(40000, 40000, 45)

man = Maneuver(orbit1, "lightseagreen")

p = OrbitPlotter(body)

p.plot(orbit2, craft, man)

p.visualize()

