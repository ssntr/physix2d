from config import np, plt, draw_config

class Simulation:
    def __init__(self, shapes, sim_time=3, delta_time=0.001, gravity=-9.81, e=1):
        self.shapes = shapes
        self.sim_time = sim_time
        self.delta_time = delta_time
        self.gravity = gravity
        self.e = e #Törmäyskerroin
        self.trajectories = {}
        self.angles = {} #trajectories ja angles -sanakirjat käytössä vain ensimmäisessä versiossa reitin piirrosta
        for shape in self.shapes:
            self.trajectories[shape] = []
            self.angles[shape] = []

        self.collision_items = None

    def handle_simulation(self):
        plt.figure(figsize=draw_config["figsize"])
        plt.xlim(draw_config["xlim"])
        plt.ylim(draw_config["ylim"])

        for shape in self.shapes:
            shape.plot()

        time = self.delta_time
        plot_interval = 0
        while time < self.sim_time - self.delta_time:
            if self.collision():
                closest_edge = self.closest_edge()
                relative_velocity = self.relative_velocity()
                collision_normal = self.collision_normal(closest_edge)

                if np.dot(relative_velocity, collision_normal) < 0:
                    impulse = self.impulse(relative_velocity, collision_normal)
                    self.update_shape_velocities(collision_normal, impulse)

            plot_interval += 1
            for shape in self.shapes:
                shape.move_shape(shape.velocity, self.delta_time)
                shape.rotate()
                if plot_interval == draw_config["plot_interval"]:
                    shape.plot()

            time += self.delta_time
            if plot_interval == draw_config["plot_interval"]:
                plot_interval = 0
        plt.show()

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
                        self.collision_items = {
                            "collision_vertex": np.array(vertex),
                            "edge_shape": edge_shape,
                            "vertex_shape": vertex_shape
                        }
                        return True

        return False

    def closest_edge(self):
        closest_edge = None
        smallest_distance = float('inf')
        collision_vertex = self.collision_items["collision_vertex"]
        edge_shape = self.collision_items["edge_shape"]

        edges = edge_shape.get_edges()
        for i, edge in enumerate(edges):
            r_EP = collision_vertex - edge_shape.vertices[i]
            norm = np.linalg.norm(edge)
            normalized_edge = edge / norm
            distance = abs(np.cross(normalized_edge, r_EP))

            if distance < smallest_distance:
                smallest_distance = distance
                closest_edge = edge

        return closest_edge


    def relative_velocity(self):
        collision_vertex = self.collision_items["collision_vertex"]
        edge_shape = self.collision_items["edge_shape"]
        vertex_shape = self.collision_items["vertex_shape"]

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

    def impulse(self, relative_velocity, collision_normal):
        edge_shape = self.collision_items["edge_shape"]
        vertex_shape = self.collision_items["vertex_shape"]
        collision_vertex = self.collision_items["collision_vertex"]

        r_AP = (collision_vertex - vertex_shape.cm())
        r_BP = (collision_vertex - edge_shape.cm())

        mass_inverse_sum = (1 / vertex_shape.mass) + (1 / edge_shape.mass)

        inertia_component_A = np.cross(r_AP, collision_normal) ** 2 / vertex_shape.j
        inertia_component_B = np.cross(r_BP, collision_normal) ** 2 / edge_shape.j

        relative_dot_product = np.dot(relative_velocity, collision_normal)

        impulse = -(1 + self.e) * (relative_dot_product / (mass_inverse_sum + inertia_component_A + inertia_component_B))
        print(f"Impulse: {impulse}")
        return impulse

    def update_shape_velocities(self, collision_normal, impulse):
        edge_shape = self.collision_items["edge_shape"]
        vertex_shape = self.collision_items["vertex_shape"]
        collision_vertex = self.collision_items["collision_vertex"]

        v_A = vertex_shape.velocity + impulse/vertex_shape.mass * collision_normal
        v_B = edge_shape.velocity - impulse/edge_shape.mass * collision_normal

        vertex_shape.velocity = v_A
        edge_shape.velocity = v_B

        AP = (collision_vertex - vertex_shape.cm())
        r_AP = np.array([AP[0], AP[1], 0])
        BP = (collision_vertex - edge_shape.cm())
        r_BP = np.array([BP[0], BP[1], 0])

        collision_normal = np.array([collision_normal[0], collision_normal[1], 0])

        updated_rot_A = vertex_shape.rotation + impulse/vertex_shape.mass * np.cross(r_AP, collision_normal)[2]
        updated_rot_B = edge_shape.rotation - impulse/edge_shape.mass * np.cross(r_BP, collision_normal)[2]

        vertex_shape.rotation = updated_rot_A
        edge_shape.rotation = updated_rot_B
        print(f"Updated rotations: {vertex_shape.rotation} and {edge_shape.rotation}")
