'''
File containing definition of Craft class and relevant constants
'''

'''
Class used for defining spacecraft to orbit a body
'''
class Craft:
    '''
    Init function takes craft's name and the craft's color
    '''
    def __init__(self, n, c):
        self.name = n
        self.color = c

'''
Sample Craft constants representing some famous crafts
'''

'''
NASA's Space Shuttle
'''
SPACE_SHUTTLE = Craft("Space Shuttle", "white")

'''
The first man-made object in orbit, the Soviet Union's Sputnik 1
'''
SPUTNIK_1 = Craft("Sputnik 1", "dimgray")

'''
The International Space Station
'''
ISS = Craft("ISS", "salmon")

'''
The Soviet Union's/Russia's Mir space station
'''
MIR = Craft("Mir", "firebrick")

'''
NASA's Skylab space station
'''
SKYLAB = Craft("Skylab", "thistle")