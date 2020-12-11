from Pyrigee import *

body = Body("Earth", 5.9722e24, 6378, "cornflowerblue")
craft = Craft("Satellite", "lime")


initial_orbit = Orbit(400, 400, 0)
target_orbit = Orbit(2000, 2000, 0)
maneuver = Maneuver(target_orbit, "firebrick")

p = OrbitPlotter(body)

# Pass maneuver to the plot function
p.plot(initial_orbit, craft, maneuver)

p.visualize()