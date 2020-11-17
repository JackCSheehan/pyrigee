'''
Main file for the Pyrigee package containing functions that allow users to plot
orbits and do other calculations
'''
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math
from orbit import *
from maneuver import ManeuverType

'''
Class containing methods and constants that allows users to graph orbits
'''
class Pyrigee:
    # The number of divisions in wireframe plots for bodies
    __PLANET_DIVS = 9j

    # The number of divisions in orbit plots
    __ORBIT_DIVS = 51

    # The number of km that each tick represents
    __TICK_VALUE = 1000

    # The difference between 1 and the eccentricity when orbit is considered parabolic
    __EPSILON_E = .1

    ''' 
    Offset for graph x/y limits to ensure graph looks proportional. Divide body by 4252 to get the offset 
    to show body proportionally by matplotlib
    '''
    __LIMIT_OFFSET_DIVISOR = 4252

    # Interval in ms for animations
    __ANIMATION_INTERVAL = 120

    '''
    Initialization code for the matplotlib graph including creation of figure, __axes, and
    color settings 
    '''
    def __init__(self):
        # Create string to hold text that will be shown on side of screen
        self.__info_text = ""

        # Standard matplotlib initialization items
        self.__fig = plt.figure()
        self.__ax = self.__fig.add_subplot(111, projection = "3d", proj_type = "ortho")
        self.__ax.format_coord = self.__format_coord
        
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

    def __format_coord(self, x, y):
        return self.__info_text

    '''
    Private helper function to plot the body given in the plot function. Takes the body to
    plot
    '''
    def __plot_body(self, body):
        # Create theta and phi values that run from 0 to 2pi and 0 to pi, respectively
        theta, phi = np.mgrid[0:2 * np.pi:self.__PLANET_DIVS, 0:np.pi:self.__PLANET_DIVS]

        '''
        Calculate x, y, and z of sphere given theta and phi ranges. Divide each radius by tick value to make sure
        that the units are correct when displayed
        '''
        x = (body.radius / self.__TICK_VALUE) * np.cos(theta) * np.sin(phi)
        y = (body.radius / self.__TICK_VALUE) * np.sin(theta) * np.sin(phi)
        z = (body.radius / self.__TICK_VALUE) * np.cos(phi)

        # Calculate graph offset to show body proportionally
        graph_offset = body.radius / self.__LIMIT_OFFSET_DIVISOR

        '''
        Set limits relative to radius of body, with offsets as needed to keep graph looking proportional.
        Each body radius is reduced to the correct unit by dividing it by a tick value
        '''
        self.__ax.set_xlim(-(body.radius / self.__TICK_VALUE) - graph_offset, (body.radius / self.__TICK_VALUE) + graph_offset)
        self.__ax.set_ylim(-(body.radius / self.__TICK_VALUE) - graph_offset, (body.radius / self.__TICK_VALUE) + graph_offset)
        self.__ax.set_zlim(-(body.radius / self.__TICK_VALUE), (body.radius / self.__TICK_VALUE))

        # Plot the body on 3D __axis
        self.__ax.plot_wireframe(x, y, z, color = body.color)

    '''
    Private helper function to animate craft orbit around body. Takes the frame given by
    the the matplotlib timer; the x, y, and y coords of an orbit, and the plot of a craft
    '''
    def __animate_craft(frame, x, y, z, craft_point, craft_text):
        # Set offsets of point
        craft_point.set_offsets(np.append(x[frame], y[frame]))
        craft_point.set_3d_properties(z[frame], "z")

        # Set offsets of text to follow point
        craft_text.set_position(np.append(x[frame], y[frame]))
        craft_text.set_3d_properties(z[frame], None)

    '''
    Private helper function that plots elliptical orbits when eccentricity is between 0 and 1.
    Takes the body, orbit, and craft to plot, the scaled eccentricity, and the semi major axis
    length. The next parameter indicates if only half the orbit should be plotted. plot_labels 
    indicates whether or not the apogee/perigee labels should be plotted. legend indicates 
    whether or not the legend should be plotted
    '''
    def __plot_elliptical_orbit(self, body, orbit, craft, eccentricity, semi_major_axis, plot_half = False, plot_labels = True, legend = True):
        # Number to multiply by pi by when bounding np.linepace. Default is -2 to plot an entire polar coordinate
        pi_multiplier = -2

        z_multiplier = 1

        # If user only wants to plot half the orbit, change pi multiplier to -1, so that np.linspace goes from 0 to pi
        if plot_half:
            pi_multiplier = -1

        # Polar equation of ellipse. Uses scaled eccentricity to draw orbit at correct size
        r = (semi_major_axis * (1 - eccentricity**2)) / (1 - eccentricity * np.cos(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS)))

        # Convert polar equations to cartesean coords based on the given orbital inclination
        x = r * np.cos(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS)) * np.cos(np.radians(orbit.inclination))
        y = r * np.sin(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS))
        z = r * np.sin(np.radians(orbit.inclination)) * np.cos(np.linspace(pi_multiplier * np.pi, 0, self.__ORBIT_DIVS))

        # Default label for craft. Needed in case user set legends to false
        craft_label = craft.name

        # If no legend should be shown, set label to blank
        if not legend:
            craft_label = ""

        # Plot the orbit after scaling x and y coords to display in the correct units on graph
        self.__ax.plot(x / self.__TICK_VALUE, y / self.__TICK_VALUE, z / self.__TICK_VALUE, zdir = "z", color = craft.color, label = craft_label)

        # If plot_labels is true, plot points and labels at orbit's apogee and perigee
        if plot_labels:
            # Plot point and text at apogee
            self.__ax.scatter(x[0] / self.__TICK_VALUE, y[0] / self.__TICK_VALUE, z[0] / self.__TICK_VALUE, color = craft.color)
            self.__ax.text(x[0] / self.__TICK_VALUE, y[0] / self.__TICK_VALUE, z[0] / self.__TICK_VALUE, "Apogee", color = "white")

            # Index of orbit coordinates of the orbit's perigee
            perigee_coord_index = int(x.size / 2)

            # Plot point and text at perigee
            self.__ax.scatter(x[perigee_coord_index] / self.__TICK_VALUE, y[perigee_coord_index] / self.__TICK_VALUE, z[perigee_coord_index] / self.__TICK_VALUE, color = craft.color)
            self.__ax.text(x[perigee_coord_index] / self.__TICK_VALUE, y[perigee_coord_index] / self.__TICK_VALUE, z[perigee_coord_index] / self.__TICK_VALUE, "Perigee", color = "white")

    '''
    Private helper function that plots parabolic orbits when the eccentricity is very close to 1
    '''
    def __plot_parabolic_orbit(self, body, orbit, craft, semi_major_axis):
        # Polar equation of ellipse. Uses scaled eccentricity to draw orbit at correct size
        r = ((orbit.perigee) * 2 + (body.radius * 2)) / (1 - np.cos(np.linspace(0, 2 * np.pi, self.__ORBIT_DIVS)))

        # Convert polar equations to cartesean coords based on the given orbital inclination
        x = r * np.cos(np.linspace(0, 2 * np.pi, self.__ORBIT_DIVS)) * np.cos(np.radians(orbit.inclination))
        y = r * np.sin(np.linspace(0, 2 * np.pi, self.__ORBIT_DIVS))
        z = r * np.sin(np.radians(orbit.inclination)) * np.cos(np.linspace(0, 2 * np.pi, self.__ORBIT_DIVS))

        # Plot the orbit after scaling x and y coords to display in the correct units on graph
        self.__ax.plot(x / self.__TICK_VALUE, y / self.__TICK_VALUE, z / self.__TICK_VALUE, zdir = "z", color = craft.color, label = craft.name)

        # Index of orbit coordinates of the orbit's perigee
        perigee_coord_index = int(x.size / 2)

        # Plot point and text at perigee
        self.__ax.scatter(x[perigee_coord_index] / self.__TICK_VALUE, y[perigee_coord_index] / self.__TICK_VALUE, z[perigee_coord_index] / self.__TICK_VALUE, color = craft.color)
        self.__ax.text(x[perigee_coord_index] / self.__TICK_VALUE, y[perigee_coord_index] / self.__TICK_VALUE, z[perigee_coord_index] / self.__TICK_VALUE, "Perigee", color = "white")

    '''
    Private method that plots a hohmann transfer orbit. Takes the body being orbited, the initial orbit,
    the craft orbiting, and the target orbit. Also changes the info text to indicate the delta-v of
    the maneuver
    '''
    def __plot_hohmann_transfer_orbit(self, body, initial_orbit, craft, maneuver):
        # Get target orbit from manuever
        target_orbit = maneuver.target_orbit

        # Calculate apogee, perigee, apoapsis, and periapsis of the transfer orbit
        transfer_apogee = target_orbit.apogee
        transfer_perigee = initial_orbit.perigee
        transfer_apoapsis = transfer_apogee + body.radius
        transfer_periapsis = transfer_perigee + body.radius

        # Calculate semi-major axis of transfer orbit
        transfer_semi_major_axis = (transfer_apoapsis + transfer_periapsis) / 2

        # Calculate eccentricity of transfer orbit
        transfer_eccentricity = (transfer_apoapsis - transfer_periapsis) / (transfer_apoapsis + transfer_periapsis)

        transfer_orbit = Orbit(target_orbit.apogee, initial_orbit.perigee, initial_orbit.inclination)

        # Plot half of an elliptical orbit to plot the Hohmann Transfer Orbit
        self.__plot_elliptical_orbit(body, transfer_orbit, craft, transfer_eccentricity, transfer_semi_major_axis, True, False, False)

        # Message to show above delta-v readout
        maneuver_message = ""

        # Determine which message to show depending on whether or not an inclination change was included
        if initial_orbit.inclination != maneuver.target_orbit.inclination:
            maneuver_message = "Hohmann Transfer (with inclination change)"
        else:
            maneuver_message = "Hohman Transfer"
        
        # Add info text about delta-v needed for this maneuver
        self.__info_text += f"{craft.name} {maneuver_message}:\nΔV Needed: {maneuver.get_delta_v(body, initial_orbit) * 1000:.2f} m/s\n"

    '''
    Private method that simply plots the arrow indicating an inclination change. Does not change the info
    text or deal directly with the maneuver. Takes the body being orbited, the orbiting craft, and the 
    initial and target orbits
    '''
    def __plot_inclination_change_arrow(self, body, craft, initial_orbit, target_orbit):
        # Scale orbit distances and body radius to ensure that the inclination arrow is plotted to scale
        scaled_body_radius = body.radius / self.__TICK_VALUE
        scaled_target_apogee = target_orbit.apogee / self.__TICK_VALUE
        scaled_target_perigee = target_orbit.perigee / self.__TICK_VALUE

        # Calculate the apoapsis/periapsis (distances from center of mass) of target orbit
        scaled_target_apoapsis = scaled_target_apogee + scaled_body_radius
        scaled_target_periapsis = scaled_target_perigee + scaled_body_radius

        # Calculate major axis of the target orbit
        scaled_target_major_axis = scaled_target_apoapsis + scaled_target_periapsis

        # Calculate semi-major axis of target orbit
        scaled_target_semi_major_axis = scaled_target_major_axis / 2

        # Calculate eccentricity of target orbit
        target_eccentricity = (scaled_target_apoapsis - scaled_target_periapsis) / (scaled_target_apoapsis + scaled_target_periapsis)

        # Calculate radius of placement of inclination arrow by using polar equation of ellipse
        r = (scaled_target_semi_major_axis * (1 - target_eccentricity**2)) / (1 - target_eccentricity * np.cos(.5 * np.pi))

        # Calculate coordinates of inclination arrow
        x = r * np.cos(.5 * np.pi) * np.cos(np.radians(target_orbit.inclination))
        y = r * np.sin(.5 * np.pi)
        z = r * np.sin(np.radians(target_orbit.inclination)) * np.cos(.5 * np.pi)

        # Calculate inclination change
        inclination_change = target_orbit.inclination - initial_orbit.inclination

        marker = ""

        # set marker type depending on direction of inclination change
        if inclination_change < 0:
            marker = "$\\downarrow$"
        else:
            marker = "$\\uparrow$"

        # Plot an arrow indicating direction of inclination change
        self.__ax.plot(x, y, z, marker = marker, markersize = 15, color = craft.color)

        # Plot text next to inclination arrow
        self.__ax.text(x, y + .5, z, f"Δi = {abs(inclination_change)}°", color = "white")

    '''
    Private helper function that calls the correct plotting function to plot the given manuever. Takes the
    body being orbited, the initial orbit, the orbiting craft making the transfer, and the manuever
    '''
    def __plot_maneuver(self, body, initial_orbit, craft, maneuver):
        # Plot orbit based on given type
        if maneuver.type == ManeuverType.HOHMANN_TRANSFER_ORBIT:
            self.__plot_hohmann_transfer_orbit(body, initial_orbit, craft, maneuver)

        # If there is an inclination difference, plot the inclination change arrow indicator
        if initial_orbit.inclination != maneuver.target_orbit.inclination:
            self.__plot_inclination_change_arrow(body, craft, initial_orbit, maneuver.target_orbit)

    '''
    Function to plot crafts and orbits. Takes a single body object that the crafts will orbit and
    a dictionary of Orbit object and Craft objects paired together. This function will graph each
    corresponding to each craft. legend indicates whether or not the legend should be plotted
    '''
    def plot(self, body, orbit, craft, maneuver = None, plot_labels = True, legend = True):
        # Plot the given body
        self.__plot_body(body)

        # Calculate the apoapsis/periapsis (distances from center of mass) of orbit
        apoapsis = orbit.apogee + body.radius
        periapsis = orbit.perigee + body.radius

        # Calculate major axis by adding apogee, perigee, and body diamter
        major_axis = apoapsis + periapsis

        # Calculate semi-major axis from major axis
        semi_major_axis = major_axis / 2

        # Calculate eccentricity of orbit
        eccentricity = (apoapsis - periapsis) / (apoapsis + periapsis)

        # If eccentricity is sufficiently close to 1, plot a parabolic orbit
        if (1 - eccentricity < self.__EPSILON_E):
            self.__plot_parabolic_orbit(body, orbit, craft, semi_major_axis)
        
        # If the eccentricity is sufficiently less than 1, plot an elliptical orbit
        else:
            self.__plot_elliptical_orbit(body, orbit, craft, eccentricity, semi_major_axis, False, plot_labels, legend)

        # If user included a manuever, plot the manuever
        if maneuver != None:
            self.__plot_maneuver(body, orbit, craft, maneuver)

            # After plotting manuever, plot orbit transferred in
            self.plot(body, maneuver.target_orbit, craft, None, False, False)

        # Set default view to see planet from convenient angle
        self.__ax.view_init(azim = 45, elev = 20)

        # Show legend for orbits of given craft if user wants to show legend
        if legend:
            self.__ax.legend(facecolor = "k", framealpha = 0, labelcolor = "white")

        self.__ax.set_title(f"Orbit around {body.name}", color = "white")

    '''
    Function to show the matplotlib window
    '''
    def visualize(self):
        plt.tight_layout()
        plt.show()