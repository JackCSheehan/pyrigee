'''
File containing the PlottingCalculator class
'''
import numpy as np
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

    # Returns SCALED coords
    def calculate_elliptical_orbit_coords(self, main_inclination, eccentricity, semi_major_axis, transfer, side_inclination):
        # Number to multiply by pi by when bounding np.linepace. Default is -2 to plot an entire polar coordinate
        pi_multiplier = -2

        # If user only wants to plot half the orbit, change pi multiplier to -1, so that np.linspace goes from 0 to pi
        if transfer:
            pi_multiplier = -1

        # Polar equation of ellipse
        r = (semi_major_axis * (1 - eccentricity**2)) / (1 - eccentricity * np.cos((np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS))))

        theta = np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS)

        # Convert polar equations to cartesean coords based on the given orbital inclination
        x = r * np.cos(theta) * np.cos(np.radians(0)) # angle = rotation about x-axis
        y = r * np.sin(theta)* np.cos(np.radians(45)) # angle = rotation about y-axis

        # USE THIS WHEN ROTATING ABOUT Y
        #z = r * np.sin(theta) * np.cos(np.radians(45)) # angle = rotation about y-axis

        # USE THIS WHEN ROTATING ABOUT X
        #z = r * np.sin(theta) * np.cos(np.radians(45)) # angle = rotation about y-axis

        # If the cosine of the side inclination results in 0, the user wants a 90 degree side inclination
        #if np.cos(side_inclination) == 0:
            # Since cos(90) = 0 and tan(90) is undefined, must set this value to close to 90 but not 90 itself
            #side_inclination = 89.999

        #if np.cos(main_inclination) == 0:
            #main_inclination = 89.999

        #z = 0

        '''
        if main_inclination == 0 and side_inclination == 0:
            x = r * np.cos(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS))
            y = r * np.sin(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS))
            z = r * 0
        elif main_inclination != 0 and side_inclination == 0:
            x = r * np.cos(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS)) * np.cos(np.radians(main_inclination))
            y = r * np.sin(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS))
            z = x * np.tan(np.radians(main_inclination))
        elif main_inclination == 0 and side_inclination != 0:
            x = r * np.cos(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS))
            y = r * np.sin(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS)) * np.cos(np.radians(side_inclination))
            z = y * np.tan(np.radians(side_inclination))
        elif main_inclination == 90 and side_inclination == 90:
            x = r * np.cos(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS))
            y = r * np.sin(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS)) * np.cos(np.radians(side_inclination))
            z = y * np.tan(np.radians(side_inclination))
            y *= 0
        else:
            x = r * np.cos(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS)) * np.cos(np.radians(main_inclination))
            y = r * np.sin(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS)) * np.cos(np.radians(side_inclination))
            z = (x * np.sin(np.radians(main_inclination)) + y * np.sin(np.radians(side_inclination)))
            print("BRUH")
            
        #elif main_inclination != 0 and side_inclination != 0:
            #z = np.sqrt(r**2 - x**2 - y**2)

            #z = (x * np.cos(np.radians(main_inclination)) + y * np.sin(np.radians(side_inclination)))
        
        '''
        '''
            z1 = z[0:int(z.size / 4)]
            z2 = z[int(z.size / 4):int(z.size / 2)]
            z3 = -z[int(z.size / 2):int(3 * z.size / 4)]
            z4 = -z[int(3 * z.size / 4):z.size]

            z = np.concatenate((z1, z2, z3, z4))
            (x * np.cos(np.radians(main_inclination)) + y * np.cos(np.radians(side_inclination)))
            '''
            #print(z)

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

        # Return the scaled coordinates of the parabolic orbit
        return self.calculate_scaled_coords(x, y, z)

    # Returns SCALED COORDS
    def calculate_inclination_change_arrow_coords(self, body_radius, inclination, apogee, perigee):
        # Calculate the apoapsis/periapsis (distances from center of mass) of target orbit where inclination arrow will be plotted
        apoapsis = apogee + body_radius
        periapsis = perigee + body_radius

        # Calculate major axis of the orbit
        major_axis = apoapsis + periapsis

        # Calculate semi-major axis of orbit
        semi_major_axis = major_axis / 2

        # Calculate eccentricity of orbit
        eccentricity = (apoapsis - periapsis) / (apoapsis + periapsis)

        # Calculate radius of placement of inclination arrow by using polar equation of ellipse
        r = (semi_major_axis * (1 - eccentricity**2)) / (1 - eccentricity * np.cos(2 * np.pi))

        # Calculate coordinates of inclination arrow
        x = r * np.cos(2 * np.pi) * np.cos(np.radians(inclination))
        y = r * np.sin(2 * np.pi)
        z = r * np.sin(np.radians(inclination)) * np.cos(1.5 * np.pi)

        # Return the scaled coordinates of the inclination change arrow
        return self.calculate_scaled_coords(x, y, z)

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
        perigee_x = 0
        perigee_y = 0
        perigee_z = 0

        return (perigee_x, perigee_y, perigee_z)

    def calculate_scaled_coords(self, x, y, z):
        return (x / self.__tick_value, y / self.__tick_value, z / self.__tick_value)

    def calculate_transfer_orbit_parameters(self, initial_orbit, target_orbit, body_radius):
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

        # Return a new orbit that represents the elliptical transfer orbit
        return (Orbit(transfer_apogee, transfer_perigee, transfer_inclination), transfer_eccentricity, transfer_semi_major_axis)