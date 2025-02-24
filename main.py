from config import plt
from shape import Shape
from simulation import Simulation


triangle = Shape([[0.2, 0], [-0.1, 0.1], [-0.1, -0.1]])

simulation = Simulation([triangle])
simulation.generate_trajectories()
simulation.draw_movement()

