'''
Example usage of Pyrigee
'''

from pyrigee import *
from body import *
from craft import *
from orbit import *
from maneuver import *

body = EARTH

craft = ISS

orbit1 = Orbit(100, 100, 0)
orbit2 = Orbit(10000, 10000, 0)

man = Maneuver("TLI", orbit2, ManeuverType.HOHMANN_TRANSFER_ORBIT)

print(body.get_std_gravitational_parameter())
#print(body.get_gravitational_acceleration(1))
#print(man.get_delta_v(body, orbit1))
#print(f"r of init orbit : {body.radius + orbit1.perigee}")
#print(f"r of final orbit: {body.radius + orbit2.perigee}")
#print(body.get_orbital_velocity(800, 7178))

p = Pyrigee()

print(f"delta-v: {man.get_delta_v(body, orbit1)} km/s")

p.plot(body, orbit1, craft, man)

p.visualize()

