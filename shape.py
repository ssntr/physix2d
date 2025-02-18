from config import np, plt
from math import sqrt

class Shape:
    def __init__(self, vertices, mass=1, velocity=np.array([0, 0]), rotation=0):
        self.vertices = np.array(vertices)
        self.mass = mass
        self.velocity = np.array(velocity)
        self.rotation = rotation
        self.angle = 0

    def draw(self):
        x_list = np.append((self.vertices[:, 0]), self.vertices[0, 0])
        y_list = np.append((self.vertices[:, 1]), self.vertices[0, 1])
        plt.plot(x_list, y_list)
        plt.show()

class Plotter:
    def __init__(self, shapes, delta_time=0.05, gravity=9.81):
        self.shapes = shapes
        self.delta_time = delta_time
        self.gravity = gravity
        self.air_resistance = 0.1
        self.trajectories = {}
        for shape in shapes:
            self.trajectories[shape] = []

    def generate_trajectories(self):
        for shape in self.shapes:
            x, y = shape.vertices.mean(axis=0)
            vx, vy = shape.velocity

            means = [np.array([x, y])]

            while means[-1][1] >= 0:
                v = sqrt(vx ** 2 + vy ** 2)

                ax = -self.air_resistance*v*vx
                ay = -self.gravity - (self.air_resistance*v*vy)
                vx += ax * self.delta_time
                vy += ay * self.delta_time

                new_mean = means[-1] + np.array([vx * self.delta_time, vy * self.delta_time])
                means.append(new_mean)

            self.trajectories[shape] = np.array(means)

    def plot_trajectories(self):
        for shape, t in self.trajectories.items():
            plt.plot(t[:, 0], t[:, 1])

        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.show()
