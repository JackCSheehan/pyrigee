import numpy as np
import mayavi.mlab as mlab

inclination = 0
__ORBIT_DIVS = 49

apogee = 400
perigee = 400
radius = 6378

major_axis = apogee + perigee + (2 * radius)

# Calculate semi-major __axis from major __axi
semi_major_axis = major_axis / 2

# Scale the apogee and perigee so that it is relative to the body itself rather than (0, 0)
scaled_apogee = apogee + radius
scaled_perigee = perigee + radius

# Calculate eccentricity of scaled orbit
scaled_eccentricity = (scaled_apogee - scaled_perigee) / (scaled_apogee + scaled_perigee)

r = (semi_major_axis * (1 - scaled_eccentricity**2)) / (1 - scaled_eccentricity * np.cos(np.linspace(0, 2 * np.pi, __ORBIT_DIVS)))

# Convert polar equations to cartesean coords based on the given orbital inclination
x = r * np.cos(np.linspace(0, 2 * np.pi, __ORBIT_DIVS)) * np.cos(np.radians(inclination))
y = r * np.sin(np.linspace(0, 2 * np.pi, __ORBIT_DIVS))
z = r * np.sin(np.radians(inclination)) * np.cos(np.linspace(0, 2 * np.pi, __ORBIT_DIVS))


mlab.points3d([0], [0], [0], [6378])
mlab.plot3d(x, y, z, tube_radius=50)


mlab.show()