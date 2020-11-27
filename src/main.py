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

orbit2 = Orbit(1000000000000000000000000, 100, 0)
#orbit1 = Orbit(40000, 40000, 25)

#man = Maneuver(orbit2, "lightseagreen")

p = Pyrigee()

p.plot(body, orbit2, craft)

p.visualize()

