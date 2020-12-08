# :earth_americas: Pyrigee
A python package for simulating orbits and calculating the delta-v needed to perform simple maneuvers.

# :memo: Getting Started
You can install Pyrigee directly using pip with this command:
```
$ pip install pyrigee
```

# :paperclip: Dependencies
* Matplotlib
* Numpy

# :computer: Examples

## :globe_with_meridians: Plotting Basic Orbits

Here is a quick demo program to introduce you to the basic Pyrigee class structure:
```
from Pyrigee import *

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
```

This will produce the following plot:
![demo1]()

## :triangular_ruler: Inclined Orbits
The third positional argument of the Orbit constructor is the inclination of the orbit **in degrees**. Providing this argument will result in the orbit being rotated about the axis of the ascending node.

For example, this:
```
orbit = Orbit(400, 400, 45)
```
...would produce the following plot:
![demo2]()

##  :milky_way: Parabolic Escape Orbits
When the eccentricity of your defined orbit becomes sufficnetly close to 1 (within `__EPSILON_E`, defined in `orbit_plotter.py`), a parabolic orbit will be plotted.

```
orbit = Orbit(4000000000, 400, 0)
```
![demo3]()

# :rocket: Maneuvers
Pyrigee will plot Hohmann Transfer Orbits, inclination changes, and combinations of both. To plot a maneuver, create a target orbit and maneuver object.

```
from Pyrigee import *

body = Body("Earth", 5.9722e24, 6378, "cornflowerblue")
craft = Craft("Satellite", "lime")

# Create an initial orbit to start at
initial_orbit = Orbit(400, 400, 0)

# Create a target orbit to maneuver to
target_orbit = Orbit(40000, 40000, 0)

# Create a maneuver object by passing the target orbit and color of manuever
maneuver = Maneuver(target_orbit, "firebrick")

p = OrbitPlotter(body)

# Pass maneuver to the plot function
p.plot(initial_orbit, craft, maneuver)

p.visualize()
```

