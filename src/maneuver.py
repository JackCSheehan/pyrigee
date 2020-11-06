'''
Class containing defintiion of Maneuver class and relevant constants
'''
import numpy as np
import math

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
        self.target_orbit = t
        self.type = ty

    '''
    Function that will perform this maneuver
    '''
    def perform():
        print("perform")

    '''
    Private helper function that calculates the delta-v needed to perform a Hohmann Transfer
    Orbit. Takes a Body object that represents object being orbited and an Orbit object 
    representing the initial orbit. Returns the total delta-v needed to perform maneuver
    '''
    def __calculate_hohmann_delta_v(self, body, initial_orbit):
        # Get the standard gravitational parameter of the body
        std_gravitational_parameter = body.get_std_gravitational_parameter()

        # r1 and r2 are the distances of initial and final orbits from origin
        r1 = initial_orbit.perigee + body.radius
        r2 = self.target_orbit.perigee + body.radius

        # Delta-v required to enter the Hohmann Transfer Orbit
        delta_v1 = math.sqrt(std_gravitational_parameter / r1) * (math.sqrt(2 * r2 / (r1 + r2)) - 1)

        # Delta-v required to exit the Hohmann Transfer Orbit
        delta_v2 = math.sqrt(std_gravitational_parameter / r2) * (1 - math.sqrt(2 * r1 / (r1 + r2)))

        # Return total delta-v needed to perform the entire Hohmann Transfer
        return delta_v1 + delta_v2

    '''
    Private helper function that calculates the delta-v needed to perform a pure inclination change.
    A pure inclination change is performed by itself without any other manuevers. Function takes
    a Body object that represents object being orbited and an Orbit object representing the initial 
    orbit
    '''
    def __calculate_inclination_change_delta_v(self, body, initial_orbit):
        # Calculate change in inclination (delta-i)
        delta_i = self.target_orbit.inclination - initial_orbit.inclination

        # Calculate the actual the apoapsis/periapsis (distances from center of mass) of orbit
        apoapsis = initial_orbit.apogee + body.radius
        periapsis = initial_orbit.perigee + body.radius

        # Calculate eccentricity of orbit
        eccentricity = (apoapsis - periapsis) / (apoapsis + periapsis)

        # WIP
    
    '''
    Private helper function that calculates the delta-v needed to perform a Bi-Elliptic Transfer.
    Takes a Body object that represents object being orbited and an Orbit object representing the 
    initial orbit
    '''
    def __calculate_bielliptic_delta_v(self, body, initial_orbit):
        # Get the standard gravitational parameter of the body
        std_gravitational_parameter = body.get_std_gravitational_parameter()

        # Get the radius of the initial orbit
        r1 = initial_orbit.perigee + body.radius

        # Get the radius of the target orbit
        r2 = self.target_orbit.perigee + body.radius

        # Apogee of transfer ellipses (arbitrarily chosen to be twice the apogee of target orbit)
        rb = self.target_orbit.apogee * 2

        # Semi-major axis of first transfer orbit
        a1 = (r1 + rb) / 2

        # Semi-major axis of second transfer orbit
        a2 = (r2 + rb) / 2

        # Delta-v needed to enter first half-elliptical transfer orbit
        delta_v1 = math.sqrt((2 * std_gravitational_parameter) / r1 - (std_gravitational_parameter / a1)) - math.sqrt(std_gravitational_parameter / r1)

        # Delta-v needed to enter second elliptical transfer orbit
        delta_v2 = math.sqrt((2 * std_gravitational_parameter) / rb - (std_gravitational_parameter / a2)) - math.sqrt((2 * std_gravitational_parameter) / rb - (std_gravitational_parameter / a1))

        # Delta-v needed to circularize the final orbit
        delta_v3 = math.sqrt((2 * std_gravitational_parameter) / r2 - (std_gravitational_parameter / a2)) - math.sqrt(std_gravitational_parameter / r2)

        # Return total delta-v needed to do this maneuver 
        return delta_v1 + delta_v2 + delta_v3

    '''
    Private helper function that calculates the delta-v needed to perform a geostationary transfer
    maneuver. Takes a Body object that represents object being orbited and an Orbit object 
    representing the initial orbit
    '''
    def __calculate_geostationary_transfer_delta_v(self, body, initial_orbit):

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
        total_delta_v = 0

        # Initialize variable to hold the standard gravitational parameter
        std_gravitational_parameter = 0

        # If the orbit is a Hohmann Transfer Orbit
        if self.type == ManeuverType.HOHMANN_TRANSFER_ORBIT:

            # Check that initial and target orbit
            if initial_orbit.apogee == initial_orbit.perigee and self.target_orbit.apogee == self.target_orbit.perigee:
                
                # Calculate total delta-v to perform this maneuver
                total_delta_v = self.__calculate_hohmann_delta_v(body, initial_orbit)

            # If the apogees and perigees are invalid for Hohmann Transfers, throw exception
            else:
                raise ValueError("Both initial and target orbits must be circular when performing a Hohmann Transfer Orbit")
        
        # If the manuever type is a Bi-Elliptic Transfer
        else if self.type == ManeuverType.BIELLIPTIC_TRANSFER

            # Check that both initial and target orbits are circular
            if initial_orbit.apogee == initial_orbit.perigee and self.target_orbit.apogee == self.target_orbit.perigee:
                
                # Calculate total delta-v to perform this maneuver
                total_delta_v = self.__calculate_bielliptic_delta_v(body, initial_orbit)

            # If the apogees and perigees are invalid for Bi-Elliptic Transfer, throw exception
            else:
                raise ValueError("Both initial and target orbits must be circular when performing a Bi-Elliptic Transfer")

        # If the manuever type is a simple inclination change
        else if self.type == ManeuverType.INCLINATION_CHANGE:

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