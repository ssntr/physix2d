from config import np, plt, draw_config
from math import sqrt

class Simulation:
    def __init__(self, shapes, sim_time=0.5, delta_time=0.05, gravity=9.81):
        self.shapes = shapes
        self.sim_time = sim_time
        self.delta_time = delta_time
        self.gravity = gravity
        self.trajectories = {}
        for shape in self.shapes:
            self.trajectories[shape] = []

    def generate_trajectories(self):
        for shape in self.shapes:
            x, y = shape.vertices.mean(axis=0)
            vx, vy = shape.velocity

            means = [np.array([x, y])]

            time = 0
            while time < self.sim_time:
                v = sqrt(vx ** 2 + vy ** 2)

                ax = v*vx
                ay = -self.gravity - (v*vy)
                vx += ax * self.delta_time
                vy += ay * self.delta_time

                new_mean = means[-1] + np.array([vx * self.delta_time, vy * self.delta_time])
                means.append(new_mean)
                time += self.delta_time

            self.trajectories[shape] = np.array(means)

    def draw_movement(self):
        plt.figure(figsize=draw_config["figsize"])
        plt.xlim(draw_config["xlim"])
        plt.ylim(draw_config["ylim"])

        for shape, trajectories in self.trajectories.items():
            initial_pos = shape.vertices.mean(axis=0)
            for t in trajectories:
                movement_vec = t - initial_pos
                shape.vertices += movement_vec

                shape.plot()


        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.show()