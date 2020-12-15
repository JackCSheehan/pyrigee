from pyrigee import *

# Create a body. Give it a name, mass, radius, and display color
body = Body("Earth", 5.9722e24, 6378, "cornflowerblue")

# Create a craft. Give it a name and a display color
craft = Craft("Space Shuttle", "white")

# Create an orbit by defining its apogee, perigee, and inclination, respectively
orbit = Orbit(400, 400, 0)

# Create a new orbit plotter to plot a body and orbits around it
p = OrbitPlotter(body)

# Plot a craft following a particular orbit using the plot function (this can be done many times)
p.plot(orbit, craft)

# Use visualize() when you're ready to see the result
p.visualize()