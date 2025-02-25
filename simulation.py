import copy

from config import np, plt, draw_config
from math import sqrt

class Simulation:
    def __init__(self, shapes, sim_time=1, delta_time=0.1, gravity=-9.81):
        self.shapes = shapes
        self.sim_time = sim_time
        self.delta_time = delta_time
        self.gravity = gravity
        self.trajectories = {}
        for shape in self.shapes:
            self.trajectories[shape] = []

    def generate_cm_trajectory(self):
        for shape in self.shapes:
            x, y = shape.cm()
            vx, vy = shape.velocity
            means = [np.array([x, y])]

            time = 0
            while time < self.sim_time:
                vy += self.gravity * self.delta_time
                new_mean = means[-1] + np.array([vx, vy]) * self.delta_time
                means.append(new_mean)
                time += self.delta_time

            self.trajectories[shape] = np.array(means)

    def draw_movement(self):
        plt.figure(figsize=draw_config["figsize"])
        plt.xlim(draw_config["xlim"])
        plt.ylim(draw_config["ylim"])

        for shape, trajectories in self.trajectories.items():
            shape_copy = copy.deepcopy(shape)
            time = 0
            for t in trajectories:
                movement_vec = t - shape.cm()
                shape_copy.vertices = shape.vertices + movement_vec

                shape_copy.angle = shape.angle + shape.rotation * time
                shape_copy.rotate()

                shape_copy.plot()
                time += self.delta_time

        plt.show()