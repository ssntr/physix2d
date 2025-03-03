import numpy

from shape import Shape
from simulation import Simulation


triangle = Shape([[-.5, .5], [-.8, .6], [-.8, .4]],
                 velocity=[1, -1], rotation=numpy.pi)

collided = False
simulation = Simulation([triangle], gravity=0)
simulation.generate_cm_trajectory()
simulation.draw_movement()
collided = simulation.floor_collision_detection(simulation.floor)
print(collided)