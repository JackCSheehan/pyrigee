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
    def __init__(m, r, c):
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
SUN = Body(1.99e30, 695700, "y")

'''
The Earth
'''
EARTH = Body(5.97e24, 6378, "b")

'''
Earth's moon
'''
MOON = Body(7.34e22, 1738, "silver")