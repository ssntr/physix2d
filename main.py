import numpy

from shape import Shape
from simulation import Simulation


triangle = Shape([[-.24, .5], [-.8, .45], [-.8, .3]],
                 velocity=[1, -1], rotation=numpy.pi)

triangle2 = Shape([[.1, .5], [-.3, .6], [-.25, .42]],
                 velocity=[-1, -1], rotation=numpy.pi)

triangle2.move_shape([0,-.11])

simulation = Simulation([triangle, triangle2], gravity=0)
simulation.draw_movement()
print(simulation.collision())