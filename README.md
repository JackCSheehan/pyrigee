# :earth_americas: Pyrigee
A python package for simulating orbits and calculating the delta-v needed to perform simple maneuvers.

# :memo: Getting Started
You can install Pyrigee directly using pip with this command:
```
$ pip install pyrigee
```

# :paperclip: Dependencies
* Matplotlib
* NumPy

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

![demo1](https://raw.githubusercontent.com/JackCSheehan/pyrigee/main/assets/demo1.png)

## :triangular_ruler: Inclined Orbits
The third positional argument of the Orbit constructor is the inclination of the orbit **in degrees**. Providing this argument will result in the orbit being rotated about the axis of the ascending node.

For example, this:
```
orbit = Orbit(400, 400, 45)
```
...would produce the following plot:

![demo2](https://raw.githubusercontent.com/JackCSheehan/pyrigee/main/assets/demo2.png)

##  :milky_way: Parabolic Escape Orbits
When the eccentricity of your defined orbit becomes sufficnetly close to 1 (within `__EPSILON_E`, defined in `orbit_plotter.py`), a parabolic orbit will be plotted.

```
orbit = Orbit(4000000000, 400, 0)
```

![demo3](https://raw.githubusercontent.com/JackCSheehan/pyrigee/main/assets/demo3.png)

# :rocket: Maneuvers
Pyrigee will plot Hohmann transfer Orbits, inclination changes, and combinations of both. To plot a maneuver, create a target orbit and maneuver object.

## :straight_ruler: Simple Maneuvers (Basic Hohmann Transfer)

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

![demo4](https://raw.githubusercontent.com/JackCSheehan/pyrigee/main/assets/demo4.png)

## :gear: Complicated Maneuvers (Transfer + Inclination Change)
Target orbits that have a different inclination than their corresponding initial orbits result in maneuvers with an inclination change.

```
initial_orbit = Orbit(400, 400, 0)
target_orbit = Orbit(2000, 2000, 45)
maneuver = Maneuver(target_orbit, "firebrick")
```

![demo5](https://raw.githubusercontent.com/JackCSheehan/pyrigee/main/assets/demo5.png)

The solid green lines represent the initial and target orbits defined for the craft (only the initial orbit is given apogee/perigee labels). The solid red line represents half of the elliptical transfer orbit taken by the craft to move from one orbit to another. Finally, the dotted line represents the orbit entered before or after an inclination change. The dotted line attempts to show the relationship between the inclination change manuever and the Hohmann transfer, which are calculated two separate maneuvers rather than a single maneuver.

In this particular example, the spacecraft will move from the inner green orbit along the solid red line until it gets to the orbit represented by the dotted red line. Next, the spacecraft will do a burn at the ascending node to incline its orbit 45 degrees, brining it to the outer green orbit.

# :chart_with_upwards_trend: Delta-V Calculations
Pyrigee automatically calculates the delta-v needed to perform manuevers. For maneuvers involving both a Hohmann transfer and an inclination change, Pyrigee will calculate the delta-v needed to do two separate maneuvers in order to take the most efficient path to the target orbit. Pyrigee will calculate inclination changes, in particular, while in the highest orbit provided. If the initial orbit is higher than the target orbit, for example, Pyrigee will do the inclination change while still in the initial orbit and vice versa. This is because inclination changes are cheapest when instantaneous velocity is lowest.

The delta-v calculations appear in the toolbar section of the Matplotlib window.

![deltav](https://raw.githubusercontent.com/JackCSheehan/pyrigee/main/assets/deltav.png)

# :bookmark: Informational Resources
Below are some helpful resources for learning more about orbits and maneuvers.
## :black_nib: Orbital Mechanics
* [Kepler's Laws](https://en.wikipedia.org/wiki/Kepler%27s_laws_of_planetary_motion)
* [Orbital Eccentricity](https://en.wikipedia.org/wiki/Orbital_eccentricity)
* [Elliptic Orbit](https://en.wikipedia.org/wiki/Elliptic_orbit)

## :pencil2: Orbital Manuevers
* [Hohmann Transfer Orbit](https://en.wikipedia.org/wiki/Hohmann_transfer_orbit)
* [Inclination Change](https://en.wikipedia.org/wiki/Orbital_inclination_change)