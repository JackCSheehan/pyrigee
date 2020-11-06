'''
File containing definition of Body class and relevent constants
'''

'''
Class used for defining bodies for spacecraft to orbit around
'''
class Body:
    # The gravitational constant
    __BIG_G = 6.67430e-11

    '''
    Init function takes body mass, radius (in km), and color
    '''
    def __init__(self, n, m, r, c):
        self.name = n
        self.mass = m
        self.radius = r
        self.color = c

    '''
    Returns the gravitational distance at the given distance (in km) from the SURFACE of this body 
    in meters/second (SI units)
    '''
    def get_gravitational_acceleration(self, distance):
        return ((self.__BIG_G * self.mass) / (((self.radius * 1000) + (distance * 1000))**2))

    '''
    Returns the standard gravitational parameter (mu = GM) for this body
    '''
    def get_std_gravitational_parameter(self):
        return self.__BIG_G * self.mass

'''
Sample Body constants representing some bodies in the universe. All radii
are based on equatorial radii
'''

'''
The Sun (Solis), the star at the center of our solar system 
'''
SUN = Body("Sun", 1.9885e30, 695700, "y")

'''
The Earth
'''
EARTH = Body("Earth", 5.9722e24, 6378, "cornflowerblue")

'''
Earth's moon
'''
MOON = Body("Moon", 7.342e22, 1738, "silver")

'''
Near-Earth asteroid Bennu
'''
BENNU = Body("Bennu", 7.329e10, 0.28, "darkgray")