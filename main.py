import numpy

from shape import Shape
from simulation import Simulation


triangle = Shape([[-.5, .5], [-.8, .6], [-.8, .4]],
                 velocity=[1, -1], rotation=numpy.pi)

simulation = Simulation([triangle], gravity=0)
simulation.generate_cm_trajectory()
simulation.draw_movement()