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
    Function that will perform this maneuver
    '''
    def perform():
        print("perform")

    '''
    Private helper function that calculates the delta-v needed to perform a a transfer between
    two difference orbital velocities and an inclination change
    '''
    def __calculate_delta_v(self, body, initial_orbit):
        # Get the standard gravitational parameter of the body
        std_gravitational_parameter = body.get_std_gravitational_parameter()

        # Calculate semi-major axis of initial orbit -- (initial apoapsis + initial periapsis) / 2
        initial_semi_major_axis = ((initial_orbit.apogee + body.radius) + (initial_orbit.perigee + body.radius)) / 2

        # Calculate semi-major axis of final orbit
        final_semi_major_axis = ((self.target_orbit.apogee + body.radius) + (self.target_orbit.perigee + body.radius)) / 2

        # Calculate orbital velocity of initial orbit
        initial_velocity = body.get_orbital_velocity(body.radius + initial_orbit.perigee, initial_semi_major_axis)

        # Calculate orbit velocity of final orbit
        final_velocity = body.get_orbital_velocity(body.radius + self.target_orbit.perigee, final_semi_major_axis)

        # Calculate change in inclination between initial and final orbit
        inclination_change = self.target_orbit.inclination - initial_orbit.inclination

        # Calculate delta-v of manuever from manuever formula with inclination change
        delta_v = math.sqrt(initial_velocity**2 + final_velocity**2 - 2 * initial_velocity * final_velocity * np.cos(inclination_change))

        return delta_v

    '''
    Calculates the total delta-v needed to do this maneuver. Takes a Body object that represents object
    being orbited and an Orbit object representing the initial orbit. If this maneuver is not a simple
    inclination change but requires an inclination change to reach its target orbit, the delta-v of
    an inclination change will be added to total delta-v
    '''
    def get_delta_v(self, body, initial_orbit):
        # Get the gravitational acceleration of the given body
        gravitation_acceleration = body.get_gravitational_acceleration(initial_orbit.perigee) 
        
        # Initialize variable to hold total delta-v
        delta_v = 0

        # Initialize variable to hold the standard gravitational parameter
        std_gravitational_parameter = 0

        # If the orbit is a Hohmann Transfer Orbit
        if self.type == ManeuverType.HOHMANN_TRANSFER_ORBIT:

            # Check that initial and target orbit
            if initial_orbit.apogee == initial_orbit.perigee and self.target_orbit.apogee == self.target_orbit.perigee:
                
                # Calculate total delta-v to perform this maneuver
                delta_v = self.__calculate_delta_v(body, initial_orbit)

            # If the apogees and perigees are invalid for Hohmann Transfers, throw exception
            else:
                raise ValueError("Both initial and target orbits must be circular when performing a Hohmann Transfer Orbit")
        
        # If the manuever type is a Bi-Elliptic Transfer
        elif self.type == ManeuverType.BIELLIPTIC_TRANSFER:

            # Check that both initial and target orbits are circular
            if initial_orbit.apogee == initial_orbit.perigee and self.target_orbit.apogee == self.target_orbit.perigee:
                
                # Calculate total delta-v to perform this maneuver
                total_delta_v = self.__calculate_bielliptic_delta_v(body, initial_orbit)

            # If the apogees and perigees are invalid for Bi-Elliptic Transfer, throw exception
            else:
                raise ValueError("Both initial and target orbits must be circular when performing a Bi-Elliptic Transfer")

        # If the manuever type is a simple inclination change
        elif self.type == ManeuverType.INCLINATION_CHANGE:

            # Check to make sure initial and final orbit shapes are the same
            if initial_orbit.apogee == self.target_orbit.apogee and initial_orbit.perigee == self.target_orbit.perigee:

                # If inclination is same between initial and final orbit, delta-v is 0
                if initial_orbit.inclination == self.target_orbit.inclination:
                    total_delta_v = 0
                
                # If there is a difference, calculate delta-v for pure inclination change
                else:
                    total_delta_v = self.__calculate_inclination_change_delta_v(body, initial_orbit)
            
            # If there is a change in shape of orbit, throw error
            else:
                raise ValueError("Shape of orbit must remain unchanged for pure inclination change maneuver")



        return total_delta_v