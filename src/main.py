'''
Example usage of Pyrigee
'''

from pyrigee import *
from body import *
from craft import *
from orbit import *

body = MOON

orbit1 = Orbit(400, 400, 0)
craft1 = ISS

orbit2 = POLAR_ORBIT
craft2 = SPACE_SHUTTLE

orbit3 = GEOSTATIONARY_ORBIT
craft3 = MIR

orbit4 = SUN_SYNCHRONOUS_ORBIT
craft4 = SKYLAB

p = Pyrigee()

orbit_craft_pair = {orbit1 : craft1}

p.plot(body, orbit1, craft1)
p.visualize()