from __future__ import print_function, division
import numpy as np
import numpy.random as random
import pandas as pd
print('import numpy.random as random')
import matplotlib.pylab as plt
from PyAstronomy.pyTiming import pyPeriod
import matplotlib
import csv
from numpy import genfromtxt
from astropy import units as u
print('from astropy import units as u')
from astropy.coordinates import SkyCoord
import pickle
from scipy.ndimage.interpolation import shift
from matplotlib import gridspec
import matplotlib.patches as patches
print('import matplotlib.patches as patches')
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.font_manager import FontProperties
from matplotlib.pyplot import Polygon
from scipy.optimize import curve_fit
from numpy.random import rand