from config import np, plt, draw_config
from shape import Shape


class Simulation:
    def __init__(self, shapes, sim_time=1, delta_time=0.1, gravity=-9.81, e=1):
        self.shapes = shapes
        self.sim_time = sim_time
        self.delta_time = delta_time
        self.gravity = gravity
        self.e = e #Törmäyskerroin
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
        for i, edge_shape in  enumerate(self.shapes):
            edges = edge_shape.get_edges()
            for j, vertex_shape in enumerate(self.shapes):
                if i == j:
                    continue

                for vertex in vertex_shape.vertices:
                    cross_products = []
                    for k in range(len(edges)):
                        reference_vertex = edge_shape.vertices[k]
                        rp = np.array(vertex - reference_vertex)
                        cross = float(np.cross(edges[k], rp))
                        cross_products.append(cross)

                    if np.all(np.array(cross_products) > 0):
                        print(f"Collision detected: vertex {vertex} inside shape {edge_shape.vertices}!")
                        return np.array(vertex), edge_shape, vertex_shape

        return False

    def closest_edge(self, collision_vertex, edge_shape):
        closest_edge = None
        smallest_distance = float('inf')

        edges = edge_shape.get_edges()
        print(edges)
        for i, edge in enumerate(edges):
            r_EP = collision_vertex - edge_shape.vertices[i]
            norm = np.linalg.norm(edge)
            normalized_edge = edge / norm
            distance = abs(np.cross(normalized_edge, r_EP))

            if distance < smallest_distance:
                smallest_distance = distance
                closest_edge = edge

        return closest_edge


    def relative_velocity(self, collision_vertex, edge_shape, vertex_shape):
        r_AP = (collision_vertex - vertex_shape.cm())
        r_BP = (collision_vertex - edge_shape.cm())

        rotation_AP = vertex_shape.rotation
        rotation_BP = edge_shape.rotation

        #This trick was in our physics material, and gets around the need to make 3d vectors
        velocity_AP_rot = np.array([-rotation_AP * r_AP[1], rotation_AP * r_AP[0]])
        velocity_BP_rot = np.array([-rotation_BP * r_BP[1], rotation_BP * r_BP[0]])

        velocity_AP = vertex_shape.velocity + velocity_AP_rot
        velocity_BP = edge_shape.velocity + velocity_BP_rot

        return velocity_AP - velocity_BP

    def collision_normal(self, closest_edge):
        edge_3d = np.array([closest_edge[0], closest_edge[1], 0])
        k = np.array([0, 0, 1])

        normal = np.cross(edge_3d, k)[:2]
        norm = np.linalg.norm(normal)

        return normal / norm if norm !=0 else normal

    def impulse(self, edge_shape, vertex_shape, relative_velocity, collision_vertex, collision_normal):
        r_AP = (collision_vertex - vertex_shape.cm())
        r_BP = (collision_vertex - edge_shape.cm())

        mass_inverse_sum = (1 / vertex_shape.mass) + (1 / edge_shape.mass)

        inertia_component_A = np.cross(r_AP, collision_normal) ** 2 / vertex_shape.j
        inertia_component_B = np.cross(r_BP, collision_normal) ** 2 / edge_shape.j

        relative_dot_product = np.dot(relative_velocity, collision_normal)

        impulse = -(1 + self.e) * (relative_dot_product / (mass_inverse_sum + inertia_component_A + inertia_component_B))

        return impulse
