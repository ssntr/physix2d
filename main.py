import numpy

from shape import Shape
from simulation import Simulation


triangle = Shape([[-.25, .5], [-.8, .6], [-.8, .4]],
                 velocity=[1, -1], rotation=numpy.pi)

triangle2 = Shape([[0, .5], [-.3, .6], [-.3, .4]],
                 velocity=[-1, -1], rotation=numpy.pi)

# This one collides
# triangle2 = Shape([[0, .5], [-.3, .6], [-.6, .5]],
#                  velocity=[-1, -1], rotation=numpy.pi)

simulation = Simulation([triangle, triangle2], gravity=0)
simulation.draw_movement()
print(simulation.collision())