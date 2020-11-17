'''
Class containing defintiion of Maneuver class and relevant constants
'''
import numpy as np
import math
from enum import Enum

'''
An enum of supported maneuver types
'''
class ManeuverType(Enum):
    HOHMANN_TRANSFER_ORBIT = 0,
    INCLINATION_CHANGE = 1,
    BIELLIPTIC_TRANSFER = 2,
    GEOSTATIONARY_TRANSFER_ORBIT = 3

'''
Class that allows users to define maneuvers to a target orbit
'''
class Maneuver:
    '''
    Takes the name of the new orbit (for legend purposes), an Orbit object
    describing the new orbit, and a ManeuverType enum of the type of 
    Maneuver to execute
    '''
    def __init__(self, n, to, ty):
        self.name = n
        self.target_orbit = to
        self.type = ty

    '''
    Private helper funcion to calculate delta-v of Hohmann Transfer Orbit
    '''
    def __calculate_hohmann_transfer_delta_v(self, body, initial_orbit):
        # Calculate orbital radii needed in delt-v equation
        r1 = initial_orbit.perigee + body.radius
        r2 = self.target_orbit.perigee + body.radius

        # Calculate delta-v needed for both phases of transfer
        delta_v1 = math.sqrt(body.get_std_gravitational_parameter() / r1) * (math.sqrt((2 * r2) / (r1 + r2)) - 1)
        delta_v2 = math.sqrt(body.get_std_gravitational_parameter() / r2) * (1 - (math.sqrt((2 * r1) / (r1 + r2))))

        return delta_v1 + delta_v2

    '''
    Private helper function that calculates the delta-v needed to do an inclination change. Takes the body being
    orbited and the inclination change between the initial and target orbit. Calculates inclination change at apogee
    of target orbit for efficiency purposes
    '''
    def __calculate_inclination_change_delta_v(self, body, inclination_change):
        # Get the standard gravitational parameter of the body being orbited
        std_gravitational_parameter = body.get_std_gravitational_parameter()

        # Calculate orbital velocity of target orbit
        velocity = math.sqrt(std_gravitational_parameter / (self.target_orbit.apogee + body.radius))

        # Calculate delta-v needed to do inclination change
        delta_v = 2 * velocity * np.sin(np.radians(inclination_change / 2))

        return delta_v


    '''
    Calculates the total delta-v needed to do this maneuver. Takes a Body object that represents object
    being orbited and an Orbit object representing the initial orbit. If this maneuver is not a simple
    inclination change but requires an inclination change to reach its target orbit, the delta-v of
    an inclination change will be added to total delta-v
    '''
    def get_delta_v(self, body, initial_orbit):
        # Initialize variable to hold total delta-v
        delta_v = 0

        # If the orbit is a Hohmann Transfer Orbit
        if self.type == ManeuverType.HOHMANN_TRANSFER_ORBIT:

            # Check that initial and target orbit are both circular
            if initial_orbit.apogee == initial_orbit.perigee and self.target_orbit.apogee == self.target_orbit.perigee:
                
                # Calculate total delta-v to perform this maneuver
                delta_v = self.__calculate_hohmann_transfer_delta_v(body, initial_orbit)

            # If the apogees and perigees are invalid for Hohmann Transfers, throw exception
            else:
                raise ValueError("Both initial and target orbits must be circular when performing a Hohmann Transfer Orbit")

        # If an inclination change is needed, calculate inclination change delta-v at target orbit apogee
        if initial_orbit.inclination != self.target_orbit.inclination:
            
            # Calculate inclination change
            inclination_change = self.target_orbit.inclination - initial_orbit.inclination

            # Add delta-v of inclination change to total delta-v
            delta_v += abs(self.__calculate_inclination_change_delta_v(body, inclination_change))

        return delta_v