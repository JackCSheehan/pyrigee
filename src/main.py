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

orbit1 = Orbit(100000, 100, 25)
orbit2 = Orbit(400, 400, 0)

man = Maneuver("Station Transfer", orbit2, ManeuverType.HOHMANN_TRANSFER_ORBIT, "lightseagreen")

p = Pyrigee()

p.plot(body, orbit1, craft)

p.visualize()

