'''
File containing OrbitPlotter class definition
'''
import matplotlib.pyplot as plt
import numpy as np
import math
from orbit import *
from craft import *

'''
Class containing methods and constants that allows users to graph orbits
'''
class OrbitPlotter:
    # The number of divisions in wireframe plots for bodies
    __PLANET_DIVS = 9j

    # The number of divisions in orbit plots
    __ORBIT_DIVS = 61

    # The number of km that each tick represents
    __TICK_VALUE = 1000

    # The difference between 1 and the eccentricity when orbit is considered parabolic
    __EPSILON_E = .1

    # Labels for orbit apogee and perigee
    __APOGEE_LABEL = "Apogee"
    __PERIGEE_LABEL = "Perigee"

    # Offset of apogee/perigee labels
    __APSIS_LABEL_OFFSET = .7

    # Offset of inclination label
    __INCLINATION_LABEL_OFFSET = 1.5

    ''' 
    Offset for graph x/y limits to ensure graph looks proportional. Divide body by 4252 to get the offset 
    to show body proportionally by matplotlib
    '''
    __LIMIT_OFFSET_DIVISOR = 4252

    '''
    Initialization code for the matplotlib graph including creation of figure, __axes, and
    color settings. Takes a Body object that all orbits will be plotted around
    '''
    def __init__(self, b):
        self.body = b

        # Create string to hold text that will be shown on side of screen
        self.__info_text = ""

        # Standard matplotlib initialization items
        self.__fig = plt.figure()
        self.__ax = self.__fig.add_subplot(111, projection = "3d", proj_type = "ortho")
        self.__ax.format_coord = self.__format_coord

        # Set default view to see planet from convenient angle
        self.__ax.view_init(azim = 45, elev = 20)
        
        # Set background colors to black
        self.__fig.patch.set_facecolor("k")
        self.__ax.set_facecolor("k")

        # Set x, y, z label to indicate that each tick is equal to the __TICK_VALUE constant
        self.__ax.set_xlabel(f"{self.__TICK_VALUE} km")
        self.__ax.set_ylabel(f"{self.__TICK_VALUE} km")
        self.__ax.set_zlabel(f"{self.__TICK_VALUE} km")

        # Change axis colors to white
        self.__ax.xaxis.label.set_color("white")
        self.__ax.yaxis.label.set_color("white")
        self.__ax.zaxis.label.set_color("white")
        self.__ax.tick_params(axis = "x", colors = "white")
        self.__ax.tick_params(axis = "y", colors = "white")
        self.__ax.tick_params(axis = "z", colors = "white")
        
        # Change grid fill transparent
        self.__ax.w_xaxis.set_pane_color((0, 0, 0, 0))
        self.__ax.w_yaxis.set_pane_color((0, 0, 0, 0))
        self.__ax.w_zaxis.set_pane_color((0, 0, 0, 0))

        # Plot the give body
        self.__plot_body()

    '''
    Function that returns the value to be shown in the toolbar on mouse hover
    '''
    def __format_coord(self, x, y):
        return self.__info_text

    '''
    Private helper function to plot the body given in the plot function
    '''
    def __plot_body(self):
        # Create theta and phi values that run from 0 to 2pi and 0 to pi, respectively
        theta, phi = np.mgrid[0:2 * np.pi:self.__PLANET_DIVS, 0:np.pi:self.__PLANET_DIVS]

        # Scale radius of body to fir in units of plot
        scaled_radius = self.body.radius / self.__TICK_VALUE

        '''
        Calculate x, y, and z of sphere given theta and phi ranges. Divide each radius by tick value to make sure
        that the units are correct when displayed
        '''
        x = scaled_radius * np.cos(theta) * np.sin(phi) 
        y = scaled_radius * np.sin(theta) * np.sin(phi)
        z = scaled_radius * np.cos(phi)

        # Calculate graph offset to show body proportionally
        graph_offset = (self.body.radius / self.__LIMIT_OFFSET_DIVISOR)

        '''
        Set limits relative to radius of body, with offsets as needed to keep graph looking proportional.
        Each body radius is reduced to the correct unit by dividing it by a tick value
        '''
        self.__ax.set_xlim(-scaled_radius - graph_offset, scaled_radius + graph_offset)
        self.__ax.set_ylim(-scaled_radius - graph_offset, scaled_radius + graph_offset)
        self.__ax.set_zlim(-scaled_radius, scaled_radius)

        # Plot the body on 3D __axis
        self.__ax.plot_wireframe(x, y, z, color = self.body.color)

    '''
    Private helper function that takes x, y, z coordinates and returns the coordinates
    as a tuple scaled by self.__TICK_VALUE
    '''
    def __get_scaled_coordinates(self, x, y, z):
        return (x / self.__TICK_VALUE, y / self.__TICK_VALUE, z / self.__TICK_VALUE)

    '''
    Private helper function that will plot apogee text given lists of x, y, and z coords, 
    the text to plot at the apogee, and the color of the apogee point to plot
    '''
    def __plot_apogee_text(self, x, y, z, color):
        # Scale apogee coordinates for plotting
        apogee_x_coord = x[0] / self.__TICK_VALUE
        apogee_y_coord = y[0] / self.__TICK_VALUE
        apogee_z_coord = z[0] / self.__TICK_VALUE

        # Plot point and text at apogee
        self.__ax.scatter(apogee_x_coord, apogee_y_coord, apogee_z_coord, color = color)
        self.__ax.text(apogee_x_coord, apogee_y_coord + self.__APSIS_LABEL_OFFSET, apogee_z_coord + self.__APSIS_LABEL_OFFSET, self.__APOGEE_LABEL, color = "white")

    '''
    Private helper function that will plot perigee text given lists of x, y, and z coords, 
    the text to plot at the perigee, and the color of the perigee point to plot
    '''
    def __plot_perigee_text(self, x, y, z, color):
        # Index of orbit coordinates of the orbit's perigee
        perigee_coord_index = int(x.size / 2)

        # Scale perigee coordinates for plotting
        perigee_x_coord = x[perigee_coord_index] / self.__TICK_VALUE
        perigee_y_coord = y[perigee_coord_index] / self.__TICK_VALUE
        perigee_z_coord = z[perigee_coord_index] / self.__TICK_VALUE

        self.__ax.scatter(perigee_x_coord, perigee_y_coord, perigee_z_coord, color = color)
        self.__ax.text(perigee_x_coord, perigee_y_coord + self.__APSIS_LABEL_OFFSET, perigee_z_coord + self.__APSIS_LABEL_OFFSET, self.__PERIGEE_LABEL, color = "white")

    '''
    Private helper function that plots elliptical orbits when eccentricity is between 0 and 1.
    Takes the orbit and craft to plot, the scaled eccentricity, and the semi major axis
    length. The next parameter indicates if this is a transfer orbit of not. If this is true, only
    half the orbit is plotted, and the label is changed to indicate a transfer. plot_labels 
    indicates whether or not the apogee/perigee labels should be plotted. legend indicates 
    whether or not the legend should be plotted. negative indicates whether or not the orbit should
    be graphed backwards (used in plotting certain cases of transfers)
    '''
    def __plot_elliptical_orbit(self, orbit, craft, eccentricity, semi_major_axis, transfer = False, plot_labels = True, legend = True, negative = False):
        # Number to multiply by pi by when bounding np.linepace. Default is -2 to plot an entire polar coordinate
        pi_multiplier = -2

        # If user only wants to plot half the orbit, change pi multiplier to -1, so that np.linspace goes from 0 to pi
        if transfer:
            pi_multiplier = -1

        # Polar equation of ellipse. Uses scaled eccentricity to draw orbit at correct size
        r = (semi_major_axis * (1 - eccentricity**2)) / (1 - eccentricity * np.cos(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS)))

        # Negate r if negative is true
        if negative:
            r *= -1

        # Convert polar equations to cartesean coords based on the given orbital inclination
        x = r * np.cos(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS)) * np.cos(np.radians(orbit.inclination))
        y = r * np.sin(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS))
        z = r * np.sin(np.radians(orbit.inclination)) * np.cos(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS))

        # Default label for craft. Needed in case user set legends to false
        craft_label = craft.name

        # If no legend should be shown, set label to blank
        if not legend:
            craft_label = ""

        # If this is a transfer, change label to reflect 
        if transfer:
            craft_label = f"{craft.name} transfer"

        # Scaled coordinates for plotting
        scaled_x, scaled_y, scaled_z = self.__get_scaled_coordinates(*(x, y, z))

        # Plot the orbit after scaling x and y coords to display in the correct units on graph
        self.__ax.plot(scaled_x, scaled_y, scaled_z, zdir = "z", color = craft.color, label = craft_label)

        # If plot_labels is true, plot points and labels at orbit's apogee and perigee
        if plot_labels:
            # Plot the apogee and apogee point of this orbit
            self.__plot_apogee_text(x, y, z, craft.color)

            # Plot the perigee and perigee point of this orbit
            self.__plot_perigee_text(x, y, z, craft.color)

    '''
    Private helper function that plots parabolic orbits when the eccentricity is very close to 1. Takes
    the orbit and craft to plot, as well as the semi-major axis of the orbit (calculated elsewhere to
    reduce redundant code)
    '''
    def __plot_parabolic_orbit(self, orbit, craft, semi_major_axis):
        # Polar equation of ellipse. Uses scaled eccentricity to draw orbit at correct size
        r = ((orbit.perigee) * 2 + (self.body.radius * 2)) / (1 - np.cos(np.linspace(0, 2 * np.pi, self.__ORBIT_DIVS)))

        # Convert polar equations to cartesean coords based on the given orbital inclination
        x = r * np.cos(np.linspace(0, 2 * np.pi, self.__ORBIT_DIVS)) * np.cos(np.radians(orbit.inclination))
        y = r * np.sin(np.linspace(0, 2 * np.pi, self.__ORBIT_DIVS))
        z = r * np.sin(np.radians(orbit.inclination)) * np.cos(np.linspace(0, 2 * np.pi, self.__ORBIT_DIVS))

        # Scaled coordinates for plotting
        scaled_x, scaled_y, scaled_z = self.__get_scaled_coordinates(*(x, y, z))

        # Plot the orbit after scaling x and y coords to display in the correct units on graph
        self.__ax.plot(scaled_x, scaled_y, scaled_z, zdir = "z", color = craft.color, label = craft.name)

        # Plot the perigee and perigee point of this orbit
        self.__plot_perigee_text(x, y, z, craft.color)

    '''
    Private method that plots a Hohmann transfer orbit. Takes the initial orbit,
    the craft orbiting, and the target orbit
    '''
    def __plot_hohmann_transfer_orbit(self, initial_orbit, craft, target_orbit):
        # Calculate apogee, perigee, apoapsis, and periapsis of the transfer orbit
        transfer_apogee = target_orbit.apogee
        transfer_perigee = initial_orbit.perigee
        transfer_apoapsis = transfer_apogee + self.body.radius
        transfer_periapsis = transfer_perigee + self.body.radius

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

        transfer_orbit = Orbit(target_orbit.apogee, initial_orbit.perigee, transfer_inclination)

        # Flag indicating whether transfer should be plotted backwards
        negative = False

        # If transfer is from larger orbit to smaller orbit, set flag to invert transfer plot
        if initial_orbit.apogee > target_orbit.apogee:
            negative = True

        # Plot half of an elliptical orbit to plot the Hohmann Transfer Orbit
        self.__plot_elliptical_orbit(transfer_orbit, craft, transfer_eccentricity, transfer_semi_major_axis, True, False, False, negative)

    '''
    Private method that simply plots the arrow indicating an inclination change. Does not change the info
    text or deal directly with the maneuver. Takes the orbiting craft and the initial and target orbits
    '''
    def __plot_inclination_change_arrow(self, craft, initial_orbit, target_orbit):
        # Variables that will store the value of the highest apogee/perigee between the initial and target orbits
        highest_apogee = 0
        highest_perigee = 0

        '''
        Determine whether the initial or target orbit is the higher one, and set the highest apogee/perigee values as needed.
        Since transfers are restricted to circular orbits, only one apsis needs to be checked
        '''
        if initial_orbit.apogee > target_orbit.apogee:
            highest_apogee = initial_orbit.apogee
            highest_perigee = initial_orbit.perigee
        else:
            highest_apogee = target_orbit.apogee
            highest_perigee = target_orbit.perigee

        # Scale orbit distances and body radius to ensure that the inclination arrow is plotted to scale
        scaled_body_radius = self.body.radius / self.__TICK_VALUE
        scaled_apogee = highest_apogee / self.__TICK_VALUE
        scaled_perigee = highest_perigee / self.__TICK_VALUE

        # Calculate the apoapsis/periapsis (distances from center of mass) of target orbit where inclination arrow will be plotted
        scaled_apoapsis = scaled_apogee + scaled_body_radius
        scaled_periapsis = scaled_perigee + scaled_body_radius

        # Calculate major axis of the orbit
        scaled_major_axis = scaled_apoapsis + scaled_periapsis

        # Calculate semi-major axis of orbit
        scaled_semi_major_axis = scaled_major_axis / 2

        # Calculate eccentricity of orbit
        eccentricity = (scaled_apoapsis - scaled_periapsis) / (scaled_apoapsis + scaled_periapsis)

        # Calculate radius of placement of inclination arrow by using polar equation of ellipse
        r = (scaled_semi_major_axis * (1 - eccentricity**2)) / (1 - eccentricity * np.cos(2 * np.pi))

        # Calculate coordinates of inclination arrow
        x = r * np.cos(2 * np.pi) * np.cos(np.radians(initial_orbit.inclination))
        y = r * np.sin(2 * np.pi)
        z = r * np.sin(np.radians(initial_orbit.inclination)) * np.cos(2 * np.pi)

        # Calculate inclination change
        inclination_change = target_orbit.inclination - initial_orbit.inclination

        marker = ""

        # set marker type depending on direction of inclination change
        if inclination_change < 0:
            marker = "$\\downarrow$"
        else:
            marker = "$\\uparrow$"

        # Plot an arrow indicating direction of inclination change
        self.__ax.plot(x, y, z, marker = marker, markersize = 15, color = craft.color, label = f"{craft.name} inclination change")

        # Plot text next to inclination arrow
        self.__ax.text(x, y + self.__INCLINATION_LABEL_OFFSET, z - self.__INCLINATION_LABEL_OFFSET, f"Δi = {abs(inclination_change)}°", color = "white")

    '''
    Private helper function that calls the correct plotting function to plot the given manuever. Takes 
    the initial orbit, the orbiting craft making the transfer, and the manuever. Also changes the info text
    based on what combination of maneuvers was done
    '''
    def __plot_maneuver(self, initial_orbit, craft, maneuver):
        # Create custom craft for manuevering to ensure correct appearance of transfer in plot
        maneuver_craft = Craft(craft.name, maneuver.color)

        # If there is a change in the orbit radius (more extensive checking is done in manuever class)
        if maneuver.target_orbit.apogee != initial_orbit.apogee:
            self.__plot_hohmann_transfer_orbit(initial_orbit, maneuver_craft, maneuver.target_orbit)

        # If there is an inclination difference, plot the inclination change arrow indicator
        if initial_orbit.inclination != maneuver.target_orbit.inclination:
            self.__plot_inclination_change_arrow(maneuver_craft, initial_orbit, maneuver.target_orbit)
        
        # Set message of info text depending on what combination of maneuvers was done
        # If there was both an inclination change and orbit radius change
        if initial_orbit.inclination != maneuver.target_orbit.inclination and initial_orbit.apogee != maneuver.target_orbit.apogee:
            maneuver_message = "Hohmann Transfer (with inclination change)"
        
        # If there was only an orbit change
        elif initial_orbit.inclination == maneuver.target_orbit.inclination and initial_orbit.apogee != maneuver.target_orbit.apogee:
            maneuver_message = "Hohman Transfer"

        # If there was only an inclination change
        else:
            maneuver_message = "Inclination Change"
        
        # Add info text about delta-v needed for this maneuver
        self.__info_text += f"{craft.name} {maneuver_message}:\nΔV Needed: {maneuver.get_delta_v(self.body, initial_orbit) * 1000:.2f} m/s\n"

    '''
    Function to plot crafts and orbits. Takes an orbit and craft to plot. If given a manuever, the maneuver
    will be plotted. plot_labgels indicates whether or not apogee/perigee lables will be plotted. legend indicates
    whether or not the legend should be plotted
    '''
    def plot(self, orbit, craft, maneuver = None, plot_labels = True, legend = True):
        # Plot the given body
        self.__plot_body()

        # Calculate the apoapsis/periapsis (distances from center of mass) of orbit
        apoapsis = orbit.apogee + self.body.radius
        periapsis = orbit.perigee + self.body.radius

        # Calculate major axis by adding apogee, perigee, and body diamter
        major_axis = apoapsis + periapsis

        # Calculate semi-major axis from major axis
        semi_major_axis = major_axis / 2

        # Calculate eccentricity of orbit
        eccentricity = (apoapsis - periapsis) / (apoapsis + periapsis)

        # If eccentricity is sufficiently close to 1, plot a parabolic orbit
        if (1 - eccentricity < self.__EPSILON_E):
            self.__plot_parabolic_orbit(orbit, craft, semi_major_axis)
        
        # If the eccentricity is sufficiently less than 1, plot an elliptical orbit
        else:
            self.__plot_elliptical_orbit(orbit, craft, eccentricity, semi_major_axis, False, plot_labels, legend)

        # If user included a manuever, plot the manuever
        if maneuver != None:
            self.__plot_maneuver(orbit, craft, maneuver)

            # After plotting manuever, plot orbit transferred in
            self.plot(maneuver.target_orbit, craft, None, False, False)

        # Show legend for orbits of given craft if user wants to show legend
        if legend:
            self.__ax.legend(facecolor = "k", framealpha = 0, labelcolor = "white")

        # Set title to indicate the main body
        self.__ax.set_title(f"Orbit around {self.body.name}", color = "white")

    '''
    Function to show the matplotlib window
    '''
    def visualize(self):
        plt.tight_layout()
        plt.show()