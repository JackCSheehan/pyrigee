'''
File containing definition of Craft class and relevant constants
'''

'''
Class used for defining spacecraft to orbit a body
'''
class Craft:
    '''
    Init function takes craft's mass (in kg)
    '''
    def __init__(m):
        self.mass = m

'''
Sample Craft constants representing some famous crafts
'''

'''
NASA's Space Shuttle. Mass based on shuttle wet mass
'''
SPACE_SHUTTLE = Craft(110,000)

'''
The first man-made object in orbit, the Soviet Union's Sputnik 1
'''
SPUTNIK_1 = Craft(84)

'''
The International Space Station
'''
ISS = Craft(420,000)

'''
The Soviet Union's/Russia's Mir space station
'''
MIR = Craft(130,000)

'''
NASA's Skylab space station. Mass not counting Apollo crew spacecraft
'''
SKYLAB = Craft(77,000)