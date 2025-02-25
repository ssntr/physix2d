from config import np, plt, draw_config


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
            time = 0
            for t in trajectories:
                shape.move_shape(t - shape.cm())

                shape.angle = shape.rotation * time
                shape.rotate()

                shape.plot()
                time += self.delta_time

        plt.show()