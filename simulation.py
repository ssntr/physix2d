from config import np, plt, draw_config


class Simulation:
    def __init__(self, shapes, sim_time=1, delta_time=0.1, gravity=-9.81,floor= -.25):
        self.shapes = shapes
        self.sim_time = sim_time
        self.delta_time = delta_time
        self.gravity = gravity
        self.trajectories = {}
        for shape in self.shapes:
            self.trajectories[shape] = []
        self.floor = floor
    def generate_cm_trajectory(self):
        for shape in self.shapes:
            x, y = shape.cm()
            vx, vy = shape.velocity
            means = [np.array([x, y]) + np.array([vx, vy]) * self.delta_time]

            time = self.delta_time
            while time < self.sim_time - self.delta_time:
                vy += self.gravity * self.delta_time
                new_mean = means[-1] + np.array([vx, vy]) * self.delta_time
                means.append(new_mean)
                time += self.delta_time

            self.trajectories[shape] = np.array(means)

    def draw_movement(self):

        plt.figure(figsize=draw_config["figsize"])
        plt.xlim(draw_config["xlim"])
        plt.ylim(draw_config["ylim"])
        plt.axhline(y=self.floor, color=draw_config["floor_color"], linestyle=draw_config["line_style"])

        for shape, trajectories in self.trajectories.items():
            shape.plot()
            for t in trajectories:
                shape.move_shape(t - shape.cm())

                shape.angle += shape.rotation * self.delta_time
                shape.rotate()

                shape.plot()

        plt.show()

    def floor_collision_detection(self, floor):

        for shape in self.shapes:
            for vertex in shape.vertices:
                if vertex[1] < floor:
                    return True
        return False

