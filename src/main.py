'''
Example usage of Pyrigee
'''

from pyrigee import *
from body import *
from craft import *
from orbit import *
#from maneuver import *

body = EARTH

craft = ISS

orbit1 = Orbit(400, 400, 0)
orbit2 = Orbit(400, 400, 78)

#man = Maneuver("TLI", target_orbit)

#print(body.get_std_gravitational_parameter() * 1000)
#print(man.get_delta_v(body, orbit1))

p = Pyrigee()

p.plot(body, orbit1, craft)
p.plot(body, orbit2, craft)

p.visualize()

