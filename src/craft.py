'''
File containing definition of Craft class and relevant constants
'''

'''
Class used for defining spacecraft to orbit a body
'''
class Craft:
    '''
    Init function takes craft's name, mass (in kg) and the craft's color
    '''
    def __init__(self, n, m, c):
        self.name = n
        self.mass = m
        self.color = c

'''
Sample Craft constants representing some famous crafts
'''

'''
NASA's Space Shuttle. Mass based on shuttle wet mass
'''
SPACE_SHUTTLE = Craft("Space Shuttle", 110000, "white")

'''
The first man-made object in orbit, the Soviet Union's Sputnik 1
'''
SPUTNIK_1 = Craft("Sputnik 1", 84, "dimgray")

'''
The International Space Station
'''
ISS = Craft("ISS", 420000, "salmon")

'''
The Soviet Union's/Russia's Mir space station
'''
MIR = Craft("Mir", 130000, "firebrick")

'''
NASA's Skylab space station. Mass not counting Apollo crew spacecraft
'''
SKYLAB = Craft("Skylab", 77000, "thistle")