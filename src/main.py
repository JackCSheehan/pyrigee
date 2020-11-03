'''
Example usage of Pyrigee
'''

import pyrigee
from body import *
from craft import *
from orbit import *

orbit = Orbit(400, 400, 0)
body = EARTH
craft = ISS

pyrigee.plot(body, orbit, craft)