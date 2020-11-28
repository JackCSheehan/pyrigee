from Pyrigee import *

# Create body and craft
body = Body("Earth", 5.9722e24, 6378, "cornflowerblue")
craft = Craft("GOES-16", "chartreuse")

# Create orbits
initial_orbit = Orbit(400, 400, 0)
target_orbit = Orbit(400, 400, 25)

maneuver = Maneuver(target_orbit, "red")

p = OrbitPlotter(body)

# When plotting, pass maneuver as third parameter
p.plot(initial_orbit, craft, maneuver)
p.visualize()