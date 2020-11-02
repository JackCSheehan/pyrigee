'''
Example usage of Pyrigee
'''

import Pyrigee
from Body import *
from Craft import *
from Orbit import *

orbit = Orbit(40000, 600, 0)
body = EARTH
craft = ISS

Pyrigee.plot(body, orbit, craft)