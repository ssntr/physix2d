from shape import Shape
from simulation import Simulation


triangle = Shape([[-.5, .5], [-.8, .45], [-.8, .3]],
                 velocity=[1, -1], rotation=3)

square = Shape([[0.8, 0.45], [0.5, 0.5],[0.55, 0.33], [0.8, 0.3]],
                          velocity=[-1, -1], rotation=-2, mass=2)


simulation = Simulation([triangle, square], gravity=0)
simulation.handle_simulation()
