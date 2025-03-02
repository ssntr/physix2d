from config import np, plt, draw_config
from shape import Shape


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

        for shape, trajectories in self.trajectories.items():
            shape.plot()
            for t in trajectories:
                shape.move_shape(t - shape.cm())

                shape.angle += shape.rotation * self.delta_time
                shape.rotate()

                shape.plot()

        plt.show()


    def collision(self):
        for i, shape in  enumerate(self.shapes):
            edges = shape.get_edges()
            for j, other_shape in enumerate(self.shapes):
                if i == j:
                    continue

                print(f"Collision between shape {shape.vertices} edges and shape {other_shape.vertices} vertices")
                for vertex in other_shape.vertices:
                    cross_products = []
                    for k in range(len(edges)):
                        reference_vertex = shape.vertices[k]
                        rp = np.array(vertex - reference_vertex)
                        cross = float(np.cross(edges[k], rp))
                        cross_products.append(cross)
                        print(f"Edge {k}: {edges[k]}, Reference: {reference_vertex}, Vertex: {vertex}, Cross: {cross}")

                    print(cross_products)

                    if np.all(np.array(cross_products) > 0):
                        print(f"Collision detected: vertex {vertex} inside shape {shape.vertices}!")
                        return True

        return False