'''
File containing the PlottingCalculator class
'''
import numpy as np
import math
from orbit import *

'''
The PlottingCalculator class contains functions that calculate coordinates for plotting
things. Used to reduce the amount of code in the OrbitPlotter class.
'''
class PlottingCalculator:
    # The number of divisions in wireframe plots for bodies
    __PLANET_DIVS = 9j

    # The number of divisions in orbit plots
    __ORBIT_DIVS = 61

    def __init__(self, t):
        self.__tick_value = t

    '''
    Calculates the x, y, z coordinates of a sphere. Used to plot the body defined by the user. Takes
    the scaled radius, or the radius of the body scaled to the graph's tick units
    '''
    def calculate_body_coords(self, scaled_radius):
        # Create theta and phi values that run from 0 to 2pi and 0 to pi, respectively
        theta, phi = np.mgrid[0:2 * np.pi:self.__PLANET_DIVS, 0:np.pi:self.__PLANET_DIVS]

        '''
        Calculate x, y, and z of sphere given theta and phi ranges. Divide each radius by tick value to make sure
        that the units are correct when displayed
        '''
        x = scaled_radius * np.cos(theta) * np.sin(phi) 
        y = scaled_radius * np.sin(theta) * np.sin(phi)
        z = scaled_radius * np.cos(phi)

        return (x, y, z)

    '''
    Calculates the coordinates of an elliptical orbit. Takes the orbits inclination, eccentricty, and semi-major axis.
    The transfer flag indicates whether or not this is a transfer orbit, in which case only half the orbit will be 
    calculated. negative indicates whether or not the orbit should be flipped. Returns the x, y, z coords of the 
    elliptical orbit scaled by __tick_value
    '''
    def calculate_elliptical_orbit_coords(self, inclination, eccentricity, semi_major_axis, transfer, negative):
        # Number to multiply by pi by when bounding np.linepace. Default is -2 to plot an entire polar coordinate
        pi_multiplier = -2

        # If user only wants to plot half the orbit, change pi multiplier to -1, so that np.linspace goes from 0 to pi
        if transfer:
            pi_multiplier = -1

        theta = np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS)

        # Convert inclination to radians
        inclination = np.radians(inclination)

        # Polar equation of ellipse
        r = (semi_major_axis * (1 - eccentricity**2)) / (1 - eccentricity * np.cos((theta)))

        # Flip orbit if negative flag is true
        if negative:
            r *= -1

        # Convert polar equations to cartesean coords based on the given orbital inclination
        x = r * np.cos(theta) * np.cos(inclination)
        y = r * np.sin(theta)
        z = x * np.tan(inclination)
        
        # Return the scaled coordinates of the elliptical orbit
        return self.calculate_scaled_coords(x, y, z)

    '''
    Calculates the coordinates of a parabolic orbit. Takes an orbit object representing the orbit and the radius of the
    body being orbited. Returns the x, y, z coords of the orbit scaled by __tick_value
    '''
    def calculate_parabolic_orbit_coords(self, orbit, body_radius):
        # Create theta value for periodic plotting
        theta = np.linspace(0, 2 * np.pi, self.__ORBIT_DIVS)

        # Polar equation of ellipse
        r = ((orbit.perigee) * 2 + (body_radius * 2)) / (1 - np.cos(theta))

        # Convert polar equations to cartesean coords based on the given orbital inclination
        x = r * np.cos(theta) * np.cos(np.radians(orbit.inclination))
        y = r * np.sin(theta)
        z = r * np.sin(np.radians(orbit.inclination)) * np.cos(theta)

        # Return the scaled coordinates of the parabolic orbit
        return self.calculate_scaled_coords(x, y, z)

    '''
    Calculates the coordinates of the ascending node. Takes the radius of the body being orbited, the orbits
    inclination, the apogee, and the perigee/ Returns the coordinates scaled by __tick_value
    '''
    def calculate_ascending_node_coords(self, body_radius, inclination, apogee, perigee):
        # Calculate the apoapsis/periapsis (distances from center of mass) of target orbit where inclination arrow will be plotted
        apoapsis = apogee + body_radius
        periapsis = perigee + body_radius

        # Calculate ascending node height
        ascending_node_height = math.sqrt(apoapsis * periapsis)

        # Return the scaled coordinates of the inclination change arrow
        return self.calculate_scaled_coords(0, -ascending_node_height, 0)

    '''
    Calculates the coordinates of the apogee text annotation. Takes the x, y, and z coordinates of the orbit, each
    as a list of numbers
    '''
    def calculate_apogee_text_coords(self, x, y, z):
        # Get coordinates of apogee text
        apogee_x = x[0]
        apogee_y = y[0]
        apogee_z = z[0]

        return (apogee_x, apogee_y, apogee_z)
    
    '''
    Calculates the coordinates of the perigee text annotation. Takes the x, y, and z coordinates of the orbit, each
    as a list of numbers
    '''
    def calculate_perigee_text_coords(self, x, y, z):
        # Index of orbit coordinates of the orbit's perigee
        perigee_coord_index = int(x.size / 2)

        # Get coordinates of perigee text
        perigee_x = x[perigee_coord_index]
        perigee_y = y[perigee_coord_index]
        perigee_z = z[perigee_coord_index]

        return (perigee_x, perigee_y, perigee_z)

    '''
    Takes three lists, each representing x, y, and z coordinates, respectively. Returns these coordinates scaled
    by __tick_value
    '''
    def calculate_scaled_coords(self, x, y, z):
        return (x / self.__tick_value, y / self.__tick_value, z / self.__tick_value)

    '''
    Calculates the orbit, eccentricity, and semi-major axis of the transfer orbit. The transfer orbit is the elliptical
    orbit that transitions from one circular orbit to another. Takes the initial orbit, the target orbit, and the radius
    of the body being orbited
    '''
    def calculate_transfer_orbit_elements(self, initial_orbit, target_orbit, body_radius):
        # Calculate apogee, perigee, apoapsis, and periapsis of the transfer orbit
        transfer_apogee = target_orbit.apogee
        transfer_perigee = initial_orbit.perigee
        transfer_apoapsis = transfer_apogee + body_radius
        transfer_periapsis = transfer_perigee + body_radius

        # Calculate semi-major axis of transfer orbit
        transfer_semi_major_axis = (transfer_apoapsis + transfer_periapsis) / 2

        # Calculate eccentricity of transfer orbit
        transfer_eccentricity = (transfer_apoapsis - transfer_periapsis) / (transfer_apoapsis + transfer_periapsis)

        # Variable to hold the inclination of the transfer orbit
        transfer_inclination = 0

        '''
        Determine whether the initial or target orbit is the higher one, and set the transfer inclination as needed.
        The transfer orbit will be plotted to show path taken either before or after an inclination change, whichever
        is most efficient
        '''
        if initial_orbit.apogee > target_orbit.apogee:
            transfer_inclination = target_orbit.inclination
        else:
            transfer_inclination = initial_orbit.inclination

        # If the transfer apogee < transfer perigee (such as when maneuvering from higher orbit to a lower orbit), flip the values
        if transfer_apogee < transfer_perigee:
            temp = transfer_apogee
            transfer_apogee = transfer_perigee
            transfer_perigee = temp

        # Return a new orbit that represents the elliptical transfer orbit, the transfer eccentricity, and the transfer semi-major axis
        return (Orbit(transfer_apogee, transfer_perigee, transfer_inclination), transfer_eccentricity, transfer_semi_major_axis)

    '''
    Calculates the orbit, eccentricity, and semi-major axis of the in-between orbit. The in-between orbit is the orbit the
    spacecraft will be in after an inclination change to show how the spacecraft will transition between inclination changes
    and Hohmann transfer orbits. Takes the initial orbit, the target orbit, and the radius of the body being orbited
    '''
    def calculate_in_between_orbit_elements(self, initial_orbit, target_orbit, body_radius):
        # Variables to hold in-between apogee and perigee
        in_between_apogee = 0
        in_between_perigee = 0

        # Variable to hold inclination of the in-between orbit
        in_between_inclination = 0

        # If maneuver shrinks the orbit
        if initial_orbit.apogee > target_orbit.apogee:
            in_between_apogee = initial_orbit.apogee
            in_between_perigee = initial_orbit.perigee
            in_between_inclination = target_orbit.inclination

        # If the maneuver expands the orbit
        else:
            in_between_apogee = target_orbit.apogee
            in_between_perigee = target_orbit.perigee
            in_between_inclination = initial_orbit.inclination

        # Calculate in-between orbit apsis
        in_between_apoapsis = in_between_apogee + body_radius
        in_between_periapsis = in_between_perigee + body_radius

        # Calculate eccentricity of in-between orbit
        in_between_eccentricity = (in_between_apoapsis - in_between_periapsis) / (in_between_apoapsis + in_between_periapsis)

        # Calculate semi-major axis of in-between orbit
        in_between_semi_major_axis = (in_between_apoapsis + in_between_periapsis) / 2

        # Return a new orbit that represents the in-between orbit, the in-between eccentricity, and the in-between semi-major axis
        return (Orbit(in_between_apogee, in_between_perigee, in_between_inclination), in_between_eccentricity, in_between_semi_major_axis)