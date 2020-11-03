'''
Main file for the Pyrigee package containing functions that allow users to plot
orbits and do other calculations
'''
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math

# The number of divisions in wireframe plots or line plots
DIVS = 15j

# The number of km that each tick represents
TICK_VALUE = 1000

''' 
Offset for graph x/y limits to ensure graph looks proportional. Divide body by 4252 to get the offset 
to show body proportionally by matplotlib
'''
LIMIT_OFFSET_DIVISOR = 4252

# Interval in ms for animations
ANIMATION_INTERVAL = 120

'''
Private helper function to plot the body given in the plot function. Takes the body to
plot and ax, which is the matplotlib 3D axes
'''
def __plot_body(body, ax):

    # Create theta and phi values that run from 0 to 2pi and 0 to pi, respectively
    theta, phi = np.mgrid[0:2 * np.pi:DIVS, 0:np.pi:DIVS]

    '''
    Calculate x, y, and z of sphere given theta and phi ranges. Divide each radius by tick value to make sure
    that the units are correct when displayed
    '''
    x = (body.radius / TICK_VALUE) * np.cos(theta) * np.sin(phi)
    y = (body.radius / TICK_VALUE) * np.sin(theta) * np.sin(phi)
    z = (body.radius / TICK_VALUE) * np.cos(phi)

    # Set x, y, z label to indicate that each tick is equal to the TICK_VALUE constant
    ax.set_xlabel(f"{TICK_VALUE} km")
    ax.set_ylabel(f"{TICK_VALUE} km")
    ax.set_zlabel(f"{TICK_VALUE} km")

    # Calculate graph offset to show body proportionally
    graph_offset = body.radius / LIMIT_OFFSET_DIVISOR

    '''
    Set limits relative to radius of body, with offsets as needed to keep graph looking proportional.
    Each body radius is reduced to the correct unit by dividing it by a tick value
    '''
    ax.set_xlim(-(body.radius / TICK_VALUE) - graph_offset, (body.radius / TICK_VALUE) + graph_offset)
    ax.set_ylim(-(body.radius / TICK_VALUE) - graph_offset, (body.radius / TICK_VALUE) + graph_offset)
    ax.set_zlim(-(body.radius / TICK_VALUE), (body.radius / TICK_VALUE))

    # Plot the body on 3D axis
    ax.plot_wireframe(x, y, z, color = body.color)

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
def plot(body, orbit, craft):

    # Standard matplotlib initialization items
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = "3d")
    
    # Set background colors to black
    fig.patch.set_facecolor("k")
    ax.set_facecolor("k")

    # Change axis colors to white
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.zaxis.label.set_color("white")
    ax.tick_params(axis = "x", colors = "white")
    ax.tick_params(axis = "y", colors = "white")
    ax.tick_params(axis = "z", colors = "white")
    
    # Change grid fill to black and grid lines to white
    ax.w_xaxis.set_pane_color((0, 0, 0, 0))
    ax.w_yaxis.set_pane_color((0, 0, 0, 0))
    ax.w_zaxis.set_pane_color((0, 0, 0, 0))
    ax.grid(color = "red")

    # Plot the given body
    __plot_body(body, ax)

    # Calculate major axis based on given apogee/perigee and the radius of the body
    major_axis = orbit.apogee + orbit.perigee + body.radius
    
    # Calculate semi-major axis based on calculated major axis
    semi_major_axis = major_axis / 2

    # Calculate distance between side and a focus (focus is at center of body, hence radius / 2 is added)
    side_to_focus_distance = orbit.perigee + (body.radius / 2)

    # Calculate distance between the center and a focus
    center_to_focus_distance = abs(semi_major_axis - side_to_focus_distance)

    # Calculate the orbit's eccentricity. Used to graph a circle, ellipse, hyperbola, or parabola
    eccentricity = center_to_focus_distance / side_to_focus_distance

    # Part of the equation to find minor axis. Equal to -F^2, the distance from center to focus squared * -1
    big_f = -(center_to_focus_distance**2)

    # If big F becomes 0 or -0, set it to 0 to avoid domain error in square root if it is -0
    if abs(big_f) == 0:
        big_f

    # Calculate minor axis from semi-major axis and distance from foci to center
    minor_axis = (2 * math.sqrt(big_f + (semi_major_axis**2)))

    # Calculate semi-minor axis from minor axis
    semi_minor_axis = minor_axis / 2

    # Scale the major and minor axes to fit with the scale of the graph
    major_axis /= TICK_VALUE
    minor_axis /= TICK_VALUE

    print(eccentricity)
    print(math.sqrt(1 - ((semi_major_axis**2) / (semi_minor_axis**2))))

    # Calculate x and y points of the orbit ellipse
    x = (semi_major_axis / TICK_VALUE) * np.cos(np.linspace(0, 2 * np.pi))
    y = (semi_minor_axis / TICK_VALUE) * np.sin(np.linspace(0, 2 * np.pi))
    #z = x * np.tan(np.radians(orbit.inclination))

    #print(z)

    orbit_offset = 0

    # If elliptical orbit, move orbit so body is in focus of orbit
    if orbit.apogee != orbit.perigee:
        orbit_offset = (semi_major_axis + body.radius) / TICK_VALUE

    # Plot orbit based on calculated coordinates and given craft color. Offset orbit to put body at focus
    orbit_plot = ax.plot(x + orbit_offset, y, zs = 0, zdir = "z", color = craft.color)

    # Plot point and text at apogee
    ax.scatter((orbit.apogee + body.radius) / TICK_VALUE, 0, 0, color = craft.color)
    ax.text((orbit.apogee + body.radius) / TICK_VALUE, 0, 0, "Apogee", color = "white")

    # Plot point and text at perigee
    ax.scatter((-orbit.perigee - body.radius) / TICK_VALUE, 0, 0, color = craft.color)
    ax.text((-orbit.perigee - body.radius) / TICK_VALUE, 0, 0, "Perigee", color = "white")

    # Plot spacecraft at apogee
    craft_point = ax.scatter((orbit.apogee + body.radius) / TICK_VALUE, 0, 0, color = craft.color)
    craft_text = ax.text((orbit.apogee + body.radius) / TICK_VALUE, 0, 0, craft.name, color = "white")

    # Animate spacecraft. Must be assigned to a variable to work
    #a = animation.FuncAnimation(fig, __animate_craft, frames = x.size, fargs = (x + orbit_offset, y, x, craft_point, craft_text), blit = False, interval = ANIMATION_INTERVAL, repeat = True)

    ax.view_init(azim = 0, elev = 90)

    # Show the matplotlib window
    plt.show()
    '''

def plot(body, orbit, craft):

    # Standard matplotlib initialization items
    fig = plt.figure()

    ax = fig.add_subplot(111, projection = "3d", proj_type = "ortho")
    
    # Set background colors to black
    fig.patch.set_facecolor("k")
    ax.set_facecolor("k")

    # Change axis colors to white
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.zaxis.label.set_color("white")
    ax.tick_params(axis = "x", colors = "white")
    ax.tick_params(axis = "y", colors = "white")
    ax.tick_params(axis = "z", colors = "white")
    
    # Change grid fill to black and grid lines to white
    ax.w_xaxis.set_pane_color((0, 0, 0, 0))
    ax.w_yaxis.set_pane_color((0, 0, 0, 0))
    ax.w_zaxis.set_pane_color((0, 0, 0, 0))
    ax.grid(color = "red")

    # Plot the given body
    __plot_body(body, ax)

    # Calculate major axis by adding apogee, perigee, and body diamter
    major_axis = orbit.apogee + orbit.perigee + (2 * body.radius)

    # Calculate semi-major axis from major axi
    semi_major_axis = major_axis / 2

    # Scale the apogee and perigee so that it is relative to the body itself rather than (0, 0)
    scaled_apogee = orbit.apogee + body.radius
    scaled_perigee = orbit.perigee + body.radius

    # Calculate eccentricity of scaled orbit
    scaled_eccentricity = (scaled_apogee - scaled_perigee) / (scaled_apogee + scaled_perigee)

    # Polar equation of ellipse. Uses scaled eccentricity to draw orbit at correct size
    r = (semi_major_axis * (1 - scaled_eccentricity**2)) / (1 - scaled_eccentricity * np.cos(np.linspace(0, 2 * np.pi)))

    # Convert polar equations to cartesean coords based on the given orbital inclination
    x = r * np.cos(np.linspace(0, 2 * np.pi)) * np.cos(np.radians(orbit.inclination))
    y = r * np.sin(np.linspace(0, 2 * np.pi))
    z = r * np.sin(np.radians(orbit.inclination)) * np.cos(np.linspace(0, 2 * np.pi))

    # Plot the orbit after scaling x and y coords to display in the correct units on graph
    orbit_plot = ax.plot(x / TICK_VALUE, y / TICK_VALUE, z / TICK_VALUE, zdir = "z", color = craft.color)

    # Set default view to see planet from convenient angle
    ax.view_init(azim = 45, elev = 20)

    # Show the matplotlib window after setting layout to tight to ensure subplot takes up as much of fig as possible
    plt.tight_layout()
    plt.show()
