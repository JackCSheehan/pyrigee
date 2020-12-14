'''
Class containing defintiion of Maneuver class and relevant constants
'''
import numpy as np
import math

'''
Class that allows users to define maneuvers to a target orbit
'''
class Maneuver:
    '''
    Takes an Orbit object describing the new orbit, and a color to change
    appearance of maneuver in plot
    '''
    def __init__(self, to, c):
        self.target_orbit = to
        self.color = c