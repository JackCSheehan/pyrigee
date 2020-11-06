'''
Class containing defintiion of Maneuver class and relevant constants
'''
import math

'''
Class that allows users to define maneuvers to a target orbit
'''
class Maneuver:
    '''
    Takes the name of the new orbit (for legend purposes) and an Orbit object
    describing the new orbit
    '''
    def __init__(self, n, t):
        self.name = n
        self.target_orbit = t

    '''
    Calculates the total delta-v needed to do the given maneuver. Takes a Body object
    representing the body being orbited and an Orbit object representing the initial orbit
    '''
    def get_delta_v(self, body, initial_orbit):
        # Get the gravitational acceleration of the given body
        gravitation_acceleration = body.get_gravitational_acceleration(initial_orbit.perigee) 
        
        # Initialize variable to hold total delta-v
        total_delta_v = 0

        # Initialize variable to hold the standard gravitational parameter
        std_gravitational_parameter = 0

        # If the orbit is circular, use a Hohmann Transfer Orbit maneuver
        if initial_orbit.apogee == initial_orbit.perigee:
            # Get the standard gravitational parameter of the body
            std_gravitational_parameter = body.get_std_gravitational_parameter()

            # r1 and r2 are the distances of initial and final orbits from origin
            r1 = initial_orbit.perigee + body.radius
            r2 = self.target_orbit.perigee + body.radius

            # Delta-v required to enter the Hohmann Transfer Orbit
            delta_v1 = math.sqrt(std_gravitational_parameter / r1) * (math.sqrt(2 * r2 / (r1 + r2)) - 1)

            # Delta-v required to exit the Hohmann Transfer Orbit
            delta_v2 = math.sqrt(std_gravitational_parameter / r2) * (1 - math.sqrt(2 * r1 / (r1 + r2)))

            # Total delta-v needed to perform the entire Hohmann Transfer
            total_delta_v = delta_v1 + delta_v2

        return total_delta_v