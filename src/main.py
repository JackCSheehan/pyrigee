'''
Example usage of Pyrigee
'''

from pyrigee import *
from body import *
from craft import *
from orbit import *
from maneuver import *

body = EARTH

craft = SPACE_SHUTTLE

orbit2 = Orbit(100, 100, 0)
orbit1 = Orbit(40000, 40000, 25)

man = Maneuver("Station Transfer", orbit2, "lightseagreen")

p = Pyrigee()

p.plot(body, orbit1, craft, man)

p.visualize()

