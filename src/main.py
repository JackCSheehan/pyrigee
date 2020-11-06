'''
Example usage of Pyrigee
'''

from pyrigee import *
from body import *
from craft import *
from orbit import *
from maneuver import *

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

orbit_craft_pair = {orbit1 : craft1}

target_orbit = Orbit(600, 600, 0)

man = Maneuver("TLI", target_orbit)

print(body.get_std_gravitational_parameter() * 1000)
print(man.get_delta_v(body, orbit1))

p.plot(body, orbit1, craft1)
p.visualize()

