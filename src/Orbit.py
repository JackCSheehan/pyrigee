'''
File containing definition of Orbit class and relevent constants
'''

from enum import Enum

'''
Class that allows users to define custom orbits
'''
class Orbit:
    '''
    Init function takes orbit apogee (in km), perigee (in km), and inclination (in degrees)
    '''
    def __init__(a, p , i):
        self.apogee = a
        self.perigee = p
        self.inclination = i

'''
Sample Orbit constants representing common orbits
'''

'''
Equatorial orbits are directly around the equator of the earth. Apogee and perigee height
based on approximate height of ISS
'''
EQUATORIAL_ORBIT = Orbit(400, 400, 0)

'''
Sun-synchronous orbit allows a spacecraft to orbit the same place on Earth at the same time
every day. Data based approximately on typical SSO parameters
'''
SUN_SYNCHRONOUS_ORBIT = Orbit(700, 700, 98)

'''
Polar orbits orbit exactly 'vertically' around the Earth, passing through the middle of the 
poles
'''
POLAR_ORBIT = Orbit(400, 400, 90)

'''
Geostationary orbits follow the rotation of the Earth
'''
GEOSTATIONARY_ORBIT = Orbit(35786, 35786, 0)