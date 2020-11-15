'''
Main file for the Pyrigee package containing functions that allow users to plot
orbits and do other calculations
'''
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math

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
        # Standard matplotlib initialization items
        self.__fig = plt.figure()
        self.__ax = self.__fig.add_subplot(111, projection = "3d", proj_type = "ortho")
        
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
    length
    '''
    def __plot_elliptical_orbit(self, body, orbit, craft, eccentricity, semi_major_axis):
        # Polar equation of ellipse. Uses scaled eccentricity to draw orbit at correct size
        r = (semi_major_axis * (1 - eccentricity**2)) / (1 - eccentricity * np.cos(np.linspace(0, 2 * np.pi, self.__ORBIT_DIVS)))

        # Convert polar equations to cartesean coords based on the given orbital inclination
        x = r * np.cos(np.linspace(0, 2 * np.pi, self.__ORBIT_DIVS)) * np.cos(np.radians(orbit.inclination))
        y = r * np.sin(np.linspace(0, 2 * np.pi, self.__ORBIT_DIVS))
        z = r * np.sin(np.radians(orbit.inclination)) * np.cos(np.linspace(0, 2 * np.pi, self.__ORBIT_DIVS))

        # Plot the orbit after scaling x and y coords to display in the correct units on graph
        self.__ax.plot(x / self.__TICK_VALUE, y / self.__TICK_VALUE, z / self.__TICK_VALUE, zdir = "z", color = craft.color, label = craft.name)

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
    Function to plot crafts and orbits. Takes a single body object that the crafts will orbit and
    a dictionary of Orbit object and Craft objects paired together. This function will graph each
    corresponding to each craft.
    '''
    def plot(self, body, orbit, craft, maneuver = None):
        # Plot the given body
        self.__plot_body(body)

        # Calculate the apoapsis/periapsis (distances from center of mass) of orbit
        apoapsis = orbit.apogee + body.radius
        periapsis = orbit.perigee + body.radius

        # Calculate major __axis by adding apogee, perigee, and body diamter
        major_axis = apoapsis + periapsis

        # Calculate semi-major __axis from major __axi
        semi_major_axis = major_axis / 2
        print(f"Semi major axis: {semi_major_axis}")

        # Calculate eccentricity of orbit
        eccentricity = (apoapsis - periapsis) / (apoapsis + periapsis)

        # If eccentricity is sufficiently close to 1, plot a parabolic orbit
        if (1 - eccentricity < self.__EPSILON_E):
            self.__plot_parabolic_orbit(body, orbit, craft, semi_major_axis)
        
        # If the eccentricity is sufficiently less than 1, plot an elliptical orbit
        else:
            self.__plot_elliptical_orbit(body, orbit, craft, eccentricity, semi_major_axis)

        # Set default view to see planet from convenient angle
        self.__ax.view_init(azim = 45, elev = 20)

        # Show legend for orbits of given craft
        self.__ax.legend(facecolor = "k", framealpha = 0, labelcolor = "white")

    '''
    Function to show the matplotlib window
    '''
    def visualize(self):
        plt.tight_layout()
        plt.show()

'''
def plot(body, orbit, craft):

    # Standard matplotlib initialization items
    fig = plt.figure()
    __ax = fig.add_subplot(111, projection = "3d")
    
    # Set background colors to black
    fig.patch.set_facecolor("k")
    __ax.set_facecolor("k")

    # Change __axis colors to white
    __ax.x__axis.label.set_color("white")
    __ax.y__axis.label.set_color("white")
    __ax.z__axis.label.set_color("white")
    __ax.tick_params(__axis = "x", colors = "white")
    __ax.tick_params(__axis = "y", colors = "white")
    __ax.tick_params(__axis = "z", colors = "white")
    
    # Change grid fill to black and grid lines to white
    __ax.w_x__axis.set_pane_color((0, 0, 0, 0))
    __ax.w_y__axis.set_pane_color((0, 0, 0, 0))
    __ax.w_z__axis.set_pane_color((0, 0, 0, 0))
    __ax.grid(color = "red")

    # Plot the given body
    __plot_body(body, __ax)

    # Calculate major __axis based on given apogee/perigee and the radius of the body
    major___axis = orbit.apogee + orbit.perigee + body.radius
    
    # Calculate semi-major __axis based on calculated major __axis
    semi_major___axis = major___axis / 2

    # Calculate distance between side and a focus (focus is at center of body, hence radius / 2 is added)
    side_to_focus_distance = orbit.perigee + (body.radius / 2)

    # Calculate distance between the center and a focus
    center_to_focus_distance = abs(semi_major___axis - side_to_focus_distance)

    # Calculate the orbit's eccentricity. Used to graph a circle, ellipse, hyperbola, or parabola
    eccentricity = center_to_focus_distance / side_to_focus_distance

    # Part of the equation to find minor __axis. Equal to -F^2, the distance from center to focus squared * -1
    big_f = -(center_to_focus_distance**2)

    # If big F becomes 0 or -0, set it to 0 to avoid domain error in square root if it is -0
    if abs(big_f) == 0:
        big_f

    # Calculate minor __axis from semi-major __axis and distance from foci to center
    minor___axis = (2 * math.sqrt(big_f + (semi_major___axis**2)))

    # Calculate semi-minor __axis from minor __axis
    semi_minor___axis = minor___axis / 2

    # Scale the major and minor __axes to fit with the scale of the graph
    major___axis /= __TICK_VALUE
    minor___axis /= __TICK_VALUE

    print(eccentricity)
    print(math.sqrt(1 - ((semi_major___axis**2) / (semi_minor___axis**2))))

    # Calculate x and y points of the orbit ellipse
    x = (semi_major___axis / __TICK_VALUE) * np.cos(np.linspace(0, 2 * np.pi))
    y = (semi_minor___axis / __TICK_VALUE) * np.sin(np.linspace(0, 2 * np.pi))
    #z = x * np.tan(np.radians(orbit.inclination))

    #print(z)

    orbit_offset = 0

    # If elliptical orbit, move orbit so body is in focus of orbit
    if orbit.apogee != orbit.perigee:
        orbit_offset = (semi_major___axis + body.radius) / __TICK_VALUE

    # Plot orbit based on calculated coordinates and given craft color. Offset orbit to put body at focus
    orbit_plot = __ax.plot(x + orbit_offset, y, zs = 0, zdir = "z", color = craft.color)

    # Plot point and text at apogee
    __ax.scatter((orbit.apogee + body.radius) / __TICK_VALUE, 0, 0, color = craft.color)
    __ax.text((orbit.apogee + body.radius) / __TICK_VALUE, 0, 0, "Apogee", color = "white")

    # Plot point and text at perigee
    __ax.scatter((-orbit.perigee - body.radius) / __TICK_VALUE, 0, 0, color = craft.color)
    __ax.text((-orbit.perigee - body.radius) / __TICK_VALUE, 0, 0, "Perigee", color = "white")

    # Plot spacecraft at apogee
    craft_point = __ax.scatter((orbit.apogee + body.radius) / __TICK_VALUE, 0, 0, color = craft.color)
    craft_text = __ax.text((orbit.apogee + body.radius) / __TICK_VALUE, 0, 0, craft.name, color = "white")

    # Animate spacecraft. Must be assigned to a variable to work
    #a = animation.FuncAnimation(fig, __animate_craft, frames = x.size, fargs = (x + orbit_offset, y, x, craft_point, craft_text), blit = False, interval = __ANIMATION_INTERVAL, repeat = True)

    __ax.view_init(azim = 0, elev = 90)

    # Show the matplotlib window
    plt.show()
    '''


