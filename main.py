import copy

import numpy

from shape import Shape
from simulation import Simulation


triangle = Shape([[-.5, .5], [-.8, .6], [-.8, .4]],
                 velocity=[1, -1], rotation=numpy.pi)

triangle2 = Shape([[0, .5], [-.3, .6], [-.3, .4]],
                 velocity=[-1, -1], rotation=numpy.pi)

simulation = Simulation([triangle, triangle2], gravity=0)
simulation.draw_movement()
print(simulation.collision())