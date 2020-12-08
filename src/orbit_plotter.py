'''
File containing OrbitPlotter class definition
'''
import matplotlib.pyplot as plt
import numpy as np
import math
from orbit import *
from craft import *
from plotting_calculator import *

'''
Class containing methods and constants that allows users to graph orbits
'''
class OrbitPlotter:
    # The number of km that each tick represents
    __TICK_VALUE = 1000

    # The difference between 1 and the eccentricity when orbit is considered parabolic
    __EPSILON_E = .1

    # Labels for orbit apogee and perigee
    __APOGEE_LABEL = "Apogee"
    __PERIGEE_LABEL = "Perigee"

    # Label for ascending node
    __ASCENDING_NODE_LABEL = "$\Omega$"

    # Offset of apogee/perigee labels
    __APSIS_LABEL_OFFSET = .7

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

        # Create PlottingCalculator instance to do coordinate calculations
        self.__calculator = PlottingCalculator(self.__TICK_VALUE)

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
        # Scale radius of body to fit in units of plot
        scaled_radius = self.body.radius / self.__TICK_VALUE
        
        x, y, z = self.__calculator.calculate_body_coords(scaled_radius)

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
    Private helper function that will plot apogee text given lists of x, y, and z coords, 
    the text to plot at the apogee, and the color of the apogee point to plot
    '''
    def __plot_apogee_text(self, x, y, z, color):
        # Get coordinates for apogee text
        apogee_x_coord, apogee_y_coord, apogee_z_coord = self.__calculator.calculate_apogee_text_coords(x, y, z)

        # Plot point and text at apogee
        self.__ax.scatter(apogee_x_coord, apogee_y_coord, apogee_z_coord, color = color)
        self.__ax.text(apogee_x_coord, apogee_y_coord + self.__APSIS_LABEL_OFFSET, apogee_z_coord + self.__APSIS_LABEL_OFFSET, self.__APOGEE_LABEL, color = "white")

    '''
    Private helper function that will plot perigee text given lists of x, y, and z coords, 
    the text to plot at the perigee, and the color of the perigee point to plot
    '''
    def __plot_perigee_text(self, x, y, z, color):
        # Get perigee coordinates for plotting
        perigee_x_coord, perigee_y_coord, perigee_z_coord = self.__calculator.calculate_perigee_text_coords(x, y, z)

        # Plot point and text at perigee
        self.__ax.scatter(perigee_x_coord, perigee_y_coord, perigee_z_coord, color = color)
        self.__ax.text(perigee_x_coord, perigee_y_coord + self.__APSIS_LABEL_OFFSET, perigee_z_coord + self.__APSIS_LABEL_OFFSET, self.__PERIGEE_LABEL, color = "white")

    '''
    Private helper function that plots elliptical orbits when eccentricity is between 0 and 1.
    Takes the orbit and craft to plot, the scaled eccentricity, and the semi major axis
    length. The next parameter indicates if this is a transfer orbit of not. If this is true, only
    half the orbit is plotted, and the label is changed to indicate a transfer. plot_labels 
    indicates whether or not the apogee/perigee labels should be plotted. legend indicates 
    whether or not the legend should be plotted. negative indicates whether or not the orbit should
    be graphed backwards (used in plotting certain cases of transfers). in_between indicates whether or not
    the current plot should be a dashed line; used when the orbit being plotted is an in-between orbit
    '''
    def __plot_elliptical_orbit(self, orbit, craft, eccentricity, semi_major_axis, transfer = False, plot_labels = True, legend = True, negative = False, in_between = False):
        # Get coordinates of elliptical orbit
        x, y, z = self.__calculator.calculate_elliptical_orbit_coords(orbit.inclination, eccentricity, semi_major_axis, transfer, negative)

        # Default label is the craft's name
        label = craft.name

        # If this is a transfer, change label to reflect 
        if transfer:
            label = f"{craft.name} transfer"

        # If this is an in-between orbit change the label to reflect
        if in_between:
            label = f"{craft.name} after inclination change"

        # If no legend should be shown, set label to blank
        if not legend:
            label = ""

        # By default, linestyle is 
        linestyle = "solid"

        # If dashed flag is true, make the marker a dotted line
        if in_between:
            linestyle = "dotted"

        # Plot the orbit after scaling x and y coords to display in the correct units on graph
        orbit = self.__ax.plot(x, y, z, zdir = "z", color = craft.color, label = label, linestyle = linestyle)

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
        # Get coordinates for plotting parabolic orbit
        x, y, z = self.__calculator.calculate_parabolic_orbit_coords(orbit, self.body.radius)

        # Plot the orbit after scaling x and y coords to display in the correct units on graph
        self.__ax.plot(x, y, z, zdir = "z", color = craft.color, label = craft.name)

        # Plot the perigee and perigee point of this orbit
        self.__plot_perigee_text(x, y, z, craft.color)

    '''
    Private method that plots a Hohmann transfer orbit. Takes the initial orbit,
    the craft orbiting, and the target orbit
    '''
    def __plot_hohmann_transfer_orbit(self, initial_orbit, craft, target_orbit):
        # Calculate the transfer orbit elements
        transfer_orbit, transfer_eccentricity, transfer_semi_major_axis = self.__calculator.calculate_transfer_orbit_elements(initial_orbit, target_orbit, self.body.radius)

        # Plot half of an elliptical orbit to plot the Hohmann Transfer Orbit
        self.__plot_elliptical_orbit(transfer_orbit, craft, transfer_eccentricity, transfer_semi_major_axis, True, False, True, False)

    '''
    Private method that plots the arrow indicating an inclination change. Does not change the info
    text or deal directly with the maneuver. Takes the orbiting craft and the initial and target orbits
    '''
    def __plot_ascending_node(self, craft, initial_orbit, target_orbit):
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

        # Get coords of inclination change arrow
        x, y, z = self.__calculator.calculate_ascending_node_coords(self.body.radius, initial_orbit.inclination, highest_apogee, highest_perigee)

        # Plot an arrow indicating direction of inclination change
        self.__ax.plot(x, y, z, marker = self.__ASCENDING_NODE_LABEL, markersize = 10, color = craft.color, label = f"{craft.name} ascending node")

    '''
    Private method that plots the in-between orbit when an inclination change is present. An in-between orbits
    attempts to show the result of inclination changes so that complicated maneuvers are easier to understand
    '''
    def __plot_in_between_orbit(self, craft, initial_orbit, target_orbit):
        # Get in-between orbit elements
        in_between_orbit, in_between_eccentricity, in_between_semi_major_axis = self.__calculator.calculate_in_between_orbit_elements(initial_orbit, target_orbit, self.body.radius)

        # Plot an in-between orbit that shows where a spacecraft will be after an inclination change. Intended to make orbit path clearer
        self.__plot_elliptical_orbit(in_between_orbit, craft, in_between_eccentricity, in_between_semi_major_axis, False, False, True, False, True)

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

        # If there is an inclination difference, plot the ascending node indicator and the in-between orbit
        if initial_orbit.inclination != maneuver.target_orbit.inclination:
            # Plot ascending node
            self.__plot_ascending_node(maneuver_craft, initial_orbit, maneuver.target_orbit)

            # Plot in-between orbit
            self.__plot_in_between_orbit(maneuver_craft, initial_orbit, maneuver.target_orbit)
        
        # Set message of info text depending on what combination of maneuvers was done
        # If there was both an inclination change and orbit radius change
        if initial_orbit.inclination != maneuver.target_orbit.inclination and initial_orbit.apogee != maneuver.target_orbit.apogee:
            maneuver_message = "Hohmann Transfer (with inclination change)"
        
        # If there was only an orbit change
        elif initial_orbit.inclination == maneuver.target_orbit.inclination and initial_orbit.apogee != maneuver.target_orbit.apogee:
            maneuver_message = "Hohmann Transfer"

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
            # If an elliptical orbit should be plotted but there is a maneuver, throw ValueError
            if maneuver:
                raise ValueError("Cannot perform manuevers when in parabolic escape orbit")

            self.__plot_parabolic_orbit(orbit, craft, semi_major_axis)
        
        # If the eccentricity is sufficiently less than 1, plot an elliptical orbit
        else:
            self.__plot_elliptical_orbit(orbit, craft, eccentricity, semi_major_axis, False, plot_labels, legend)

        # If user included a manuever, plot the manuever
        if maneuver != None:
            self.__plot_maneuver(orbit, craft, maneuver)

            # Create transferred orbit to plot after plotting transfer
            transferred_orbit = Orbit(maneuver.target_orbit.apogee, maneuver.target_orbit.perigee, maneuver.target_orbit.inclination)

            # After plotting manuever, plot orbit transferred into
            self.plot(transferred_orbit, craft, None, False, False)

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