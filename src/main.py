'''
Example usage of Pyrigee
'''

from pyrigee import *
from body import *
from craft import *
from orbit import *
from maneuver import *

body = SUN

craft = ISS

orbit1 = Orbit(400, 400, 0)
orbit2 = Orbit(800, 800, 0)

man = Maneuver("TLI", orbit2, ManeuverType.HOHMANN_TRANSFER_ORBIT)

print(body.get_std_gravitational_parameter())
print(body.get_gravitational_acceleration(1))
print(man.get_delta_v(body, orbit1))

p = Pyrigee()

p.plot(body, orbit1, craft)
p.plot(body, orbit2, craft)

p.visualize()

