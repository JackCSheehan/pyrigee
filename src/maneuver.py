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
    Takes the name of the new orbit (for legend purposes), an Orbit object
    describing the new orbit, and a color to change appearance of maneuver 
    in plot
    '''
    def __init__(self, to, c):
        self.target_orbit = to
        self.color = c

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

        return abs(delta_v1) + abs(delta_v2)

    def __calculate_combined_delta_v(self, body, initial_orbit, inclination_change):
        # Calculate before and after semi-major axis
        initial_semi_major_axis = initial_orbit.apogee + initial_orbit.perigee + body.radius
        target_semi_major_axis = self.target_orbit.apogee + self.target_orbit.perigee + body.radius

        # Calculate the initial and final orbital velocities
        initial_vel = body.get_orbital_velocity(initial_orbit.apogee, initial_semi_major_axis)
        final_vel = body.get_orbital_velocity(self.target_orbit.apogee, target_semi_major_axis)

        # Return the result of the combined maneuver delta-v equation
        return math.sqrt(initial_vel**2 + final_vel**2 - 2 * initial_vel * final_vel * np.cos(np.radians(inclination_change)))

    '''
    Private helper function that calculates the delta-v needed to do an inclination change. Takes the body being
    orbited, the initial orbit, and the inclination change between the initial and target orbit. Calculates inclination 
    change at the ascending node of the higher of the two orbits to ensure the minimum orbit velocity during the manuever
    '''
    def __calculate_inclination_change_delta_v(self, body, initial_orbit, inclination_change):
        # Get the standard gravitational parameter of the body being orbited
        std_gravitational_parameter = body.get_std_gravitational_parameter()

        # Var to hold the highest of the two ascending nodes
        highest_ascending_node_height= 0

        # Calculate ascending node height of the initial orbit
        initial_orbit_apoapsis =  initial_orbit.apogee + body.radius
        initial_orbit_periapsis = initial_orbit.perigee + body.radius
        initial_orbit_ascending_node_height = math.sqrt(initial_orbit_apoapsis * initial_orbit_periapsis) - body.radius

        # Calculate ascending node height of the target orbit
        target_orbit_apoapsis =  self.target_orbit.apogee + body.radius
        target_orbit_periapsis = self.target_orbit.perigee + body.radius
        target_orbit_ascending_node_height = math.sqrt(target_orbit_apoapsis * target_orbit_periapsis) - body.radius

        # Determine the highest ascending node height
        if initial_orbit_ascending_node_height > target_orbit_ascending_node_height:
            highest_ascending_node_height = initial_orbit_ascending_node_height
        else:
            highest_ascending_node_height = target_orbit_ascending_node_height

        # Calculate orbital velocity of highest ascending node
        velocity = math.sqrt(std_gravitational_parameter / (highest_ascending_node_height + body.radius))

        # Calculate delta-v needed to do inclination change
        delta_v = 2 * velocity * np.sin(np.radians(inclination_change / 2))

        return abs(delta_v)


    '''
    Calculates the total delta-v needed to do this maneuver. Takes a Body object that represents object
    being orbited and an Orbit object representing the initial orbit. If this maneuver is not a simple
    inclination change but requires an inclination change to reach its target orbit, the delta-v of
    an inclination change will be added to total delta-v
    '''
    def get_delta_v(self, body, initial_orbit):
        # Initialize variable to hold total delta-v
        delta_v = 0

        # Flags used to keep track of what kind of maneuver is being performed
        transfer = False
        has_inclination_change = False
        only_circular = False

        # Set inclination flag if there is an inclination change
        if initial_orbit.inclination != self.target_orbit.inclination:
            has_inclination_change = True

        # If corresponding orbital elements are not the same, then flip the transfer flag
        if initial_orbit.apogee != target_orbit.apogee or initial_orbit.perigee != target_orbit.perigee:
            transfer = True

        # If both orbits are circular, flip the only circular flag
        if initial_orbit.apogee == initial_orbit.perigee and self.target_orbit.apogee == self.target_orbit.perigee:
            only_circular = True

        # If there is only a Hohmann transfer
        if transfer and not has_inclination_change:
            print("ONLY HOHMANN")

        # If there is only an inclination change
        elif has_inclination_change and not transfer:
            print("ONLY INCLINATION")

        # If there is both an inclination change and a Hohmann transfer
        elif transfer and has_inclination_change:
            print("BOTH")

        # Check that initial and target orbit are both circular (required to do a Hohmann transfer)
        if initial_orbit.apogee == initial_orbit.perigee and self.target_orbit.apogee == self.target_orbit.perigee:
            
            # If transfer only
            delta_v = self.__calculate_hohmann_transfer_delta_v(body, initial_orbit)

            # If inclination only
            delta_v = self.__calculate_inclination_change_delta_v(body, initial_orbit, inclination_change)

            # If transfer + inclination (should be less than Hohmann + inclination as two different things)
            delta_v = self.__calculate_combined_delta_v(body, initial_orbit, inclination_change)

        # If an inclination change is needed, calculate inclination change delta-v at target orbit apogee
        if initial_orbit.inclination != self.target_orbit.inclination:
            
            # Calculate inclination change
            inclination_change = self.target_orbit.inclination - initial_orbit.inclination

            # Add delta-v of inclination change to total delta-v
            delta_v = self.__calculate_inclination_change_delta_v(body, initial_orbit, inclination_change)

        return delta_v