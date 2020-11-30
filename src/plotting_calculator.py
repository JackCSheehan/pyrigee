'''
File containing the PlottingCalculator class
'''
import numpy as np

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

    # Returns SCALED coords
    def calculate_elliptical_orbit_coords(self, main_inclination, eccentricity, semi_major_axis, transfer, negative, side_inclination):
        # Number to multiply by pi by when bounding np.linepace. Default is -2 to plot an entire polar coordinate
        pi_multiplier = -2

        # If user only wants to plot half the orbit, change pi multiplier to -1, so that np.linspace goes from 0 to pi
        if transfer:
            pi_multiplier = -1

        # Polar equation of ellipse
        r = (semi_major_axis * (1 - eccentricity**2)) / (1 - eccentricity * np.cos((np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS))))

        # Try this
        # http://jwilson.coe.uga.edu/EMAT6680Fa05/Murray/A11/A11.html

        # Negate r if negative is true
        if negative:
            r *= -1

        # If the cosine of the side inclination results in 0, the user wants a 90 degree side inclination
        if np.cos(side_inclination) == 0:
            # Since cos(90) = 0 and tan(90) is undefined, must set this value to close to 90 but not 90 itself
            side_inclination = 89.999

        # Convert polar equations to cartesean coords based on the given orbital inclination
        x = r * np.cos(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS)) * np.cos(np.radians(main_inclination))
        y = r * np.sin(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS)) * np.cos(np.radians(side_inclination))
        z = r * np.sin(np.radians(main_inclination)) * np.cos(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS))

        if side_inclination != 0:
            z = y * np.tan(np.radians(side_inclination))

        # Return the scaled coordinates of the elliptical orbit
        return self.calculate_scaled_coords(x, y, z)

    # Returns SCALED coords
    def calculate_parabolic_orbit_coords(self, orbit, body_radius):
        # Polar equation of ellipse
        r = ((orbit.perigee) * 2 + (body_radius * 2)) / (1 - np.cos(np.linspace(0, 2 * np.pi, self.__ORBIT_DIVS)))

        # Convert polar equations to cartesean coords based on the given orbital inclination
        x = r * np.cos(np.linspace(0, 2 * np.pi, self.__ORBIT_DIVS)) * np.cos(np.radians(orbit.inclination))
        y = r * np.sin(np.linspace(0, 2 * np.pi, self.__ORBIT_DIVS))
        z = r * np.sin(np.radians(orbit.inclination)) * np.cos(np.linspace(0, 2 * np.pi, self.__ORBIT_DIVS))

        # Return the scaled coordinates of the elliptical orbit
        return self.calculate_scaled_coords(x, y, z)

    def calculate_inclination_change_arrow_coords(self):
        print()

    def calculate_apogee_text_coords(self, x, y, z):
        # Get coordinates of apogee text
        apogee_x = x[0]
        apogee_y = y[0]
        apogee_z = z[0]

        return (apogee_x, apogee_y, apogee_z)
    
    def calculate_perigee_text_coords(self, x, y, z):
        # Index of orbit coordinates of the orbit's perigee
        perigee_coord_index = int(x.size / 2)

        # Get coordinates of perigee text
        perigee_x = x[perigee_coord_index]
        perigee_y = y[perigee_coord_index]
        perigee_z = z[perigee_coord_index]

        return (perigee_x, perigee_y, perigee_z)

    def calculate_scaled_coords(self, x, y, z):
        return (x / self.__tick_value, y / self.__tick_value, z / self.__tick_value)
