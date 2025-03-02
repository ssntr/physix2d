import numpy

from shape import Shape
from simulation import Simulation


triangle = Shape([[-.24, .5], [-.8, .45], [-.8, .3]],
                 velocity=[1, -1], rotation=numpy.pi)

triangle2 = Shape([[.1, .5], [-.3, .6], [-.25, .42]],
                 velocity=[-1, 1], rotation=numpy.pi)

triangle2.move_shape([-.4, -.25])

simulation = Simulation([triangle, triangle2], gravity=0)
simulation.draw_movement()
vertex, edgeshape, vertexshape = simulation.collision()

relative_velocity = simulation.relative_velocity(vertex, edgeshape, vertexshape)
closest_edge = simulation.closest_edge(vertex, edgeshape)
collision_normal = simulation.collision_normal(closest_edge)

print(simulation.impulse(edgeshape, vertexshape, relative_velocity, vertex, collision_normal))