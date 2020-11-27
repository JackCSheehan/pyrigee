'''
Main file for the Pyrigee package that handles importing of relevant files
'''
from orbit_plotter import *
from body import *
from craft import *
from orbit import *
from maneuver import *

# Ignore RuntimeWarning that may result when plotting parabolic orbit (since there is theoretically no end to plot)
warnings.filterwarnings("ignore", category = RuntimeWarning)