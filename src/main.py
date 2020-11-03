'''
Example usage of Pyrigee
'''

import Pyrigee
from Body import *
from Craft import *
from Orbit import *

orbit = Orbit(400, 400, 25)
body = EARTH
craft = ISS

Pyrigee.plot(body, orbit, craft)