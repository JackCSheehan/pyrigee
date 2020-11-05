'''
Example usage of Pyrigee
'''

from pyrigee import *
from body import *
from craft import *
from orbit import *

body = EARTH

orbit1 = Orbit(400, 400, 0)
craft1 = ISS

orbit2 = POLAR_ORBIT
craft2 = SPACE_SHUTTLE

orbit3 = GEOSTATIONARY_ORBIT
craft3 = MIR

orbit4 = SUN_SYNCHRONOUS_ORBIT
craft4 = SKYLAB

p = Pyrigee()

orbit_craft_pair = {orbit1 : craft1, orbit2 : craft2, orbit3 : craft3, orbit4 : craft4}

p.plot(body, orbit_craft_pair)
p.visualize()