'''
File containing definition of Body class and relevent constants
'''

'''
Class used for defining bodies for spacecraft to orbit around
'''
class Body:
    
    '''
    Init function takes body mass, radius (in km), and color
    '''
    def __init__(self, n, m, r, c):
        self.name = n
        self.mass = m
        self.radius = r
        self.color = c

'''
Sample Body constants representing some bodies in the universe. All radii
are based on equatorial radii
'''

'''
The Sun (Solis), the star at the center of our solar system 
'''
SUN = Body("Sun", 1.99e30, 695700, "y")

'''
The Earth
'''
EARTH = Body("Earth", 5.97e24, 6378, "cornflowerblue")

'''
Earth's moon
'''
MOON = Body("Moon", 7.34e22, 1738, "silver")

'''
Near-Earth asteroid Bennu
'''
BENNU = Body("Bennu", 78e9, 0.28, "darkgray")