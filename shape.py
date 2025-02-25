from config import np, plt, draw_config
from math import sqrt
from math import sin
from math import cos
class Shape:
    def __init__(self, vertices, mass=1, velocity=np.array([0, 0]), rotation=0):
        self.vertices = np.array(vertices)
        self.mass = mass
        self.velocity = np.array(velocity)
        self.rotation = rotation
        self.angle = 0

    def cm(self):
        return self.vertices.mean(axis=0)

    def cm_in_origin(self):
        vector_to_origin = np.array([0, 0]) - self.cm()
        return self.vertices + vector_to_origin

    def plot(self):
        plt.plot(
            np.append(self.vertices[:, 0], self.vertices[0, 0]),
            np.append(self.vertices[:, 1], self.vertices[0, 1])
        )

        for i in range(len(self.vertices)):
            label = chr(65 + i)
            plt.text(self.vertices[i, 0], self.vertices[i, 1], label,
                     fontsize=draw_config["fontsize"],
                     ha="right", va="bottom", color=draw_config["txt_color"])

    def draw(self):
        plt.figure(figsize=draw_config["figsize"])
        plt.xlim(draw_config["xlim"])
        plt.ylim(draw_config["ylim"])
        self.plot()
        plt.show()

    def rotate_x(self, angle):
        rotated_verts = []
        for vert in self.vertices:
            y = vert[0] * cos(self.rotation * angle) - vert[1] * sin(self.rotation * angle)
            z = vert[0] * sin(self.rotation * angle) + vert[1] * cos(self.rotation * angle)
            rotated_verts.append([z, y])
        self.vertices = rotated_verts


# class Plotter:
#     def __init__(self, shapes, delta_time=0.05, gravity=9.81):
#         self.shapes = shapes
#         self.delta_time = delta_time
#         self.gravity = gravity
#         self.air_resistance = 0.1
#         self.trajectories = {}
#         for shape in shapes:
#             self.trajectories[shape] = []
#
#     def generate_trajectories(self):
#         for shape in self.shapes:
#             x, y = shape.vertices.mean(axis=0)
#             vx, vy = shape.velocity
#
#             means = [np.array([x, y])]
#
#             while means[-1][1] >= 0:
#                 v = sqrt(vx ** 2 + vy ** 2)
#
#                 ax = -self.air_resistance*v*vx
#                 ay = -self.gravity - (self.air_resistance*v*vy)
#                 vx += ax * self.delta_time
#                 vy += ay * self.delta_time
#
#                 new_mean = means[-1] + np.array([vx * self.delta_time, vy * self.delta_time])
#                 means.append(new_mean)
#
#             self.trajectories[shape] = np.array(means)
#
#     def plot_trajectories(self):
#         for shape, t in self.trajectories.items():
#             plt.plot(t[:, 0], t[:, 1])
#
#         plt.xlabel("x (m)")
#         plt.ylabel("y (m)")
#         plt.show()
