from config import plt
from shape import Shape, Plotter


triangle = Shape([[0.2, 0], [-0.1, 0.1], [-0.1, -0.1]])
dot = Shape([[0, 0]], velocity=[15.75, 25.53])

triangle.draw()
#triangle.rotate_x(90)
triangle.draw()
plotter = Plotter([dot])
plotter.generate_trajectories()
plotter.plot_trajectories()
