from config import np, plt, draw_config

class Shape:
    def __init__(self, vertices, mass=1, velocity=np.array([0, 0]), rotation=0):
        self.vertices = np.array(vertices)
        self.mass = mass
        self.velocity = np.array(velocity)
        self.rotation = rotation
        self.angle = 0
        self.reference_vertices = self.cm_in_origin().copy()

    def cm(self):
        return self.vertices.mean(axis=0)

    def cm_in_origin(self):
        vector_to_origin = np.array([0, 0]) - self.cm()
        return self.vertices + vector_to_origin

    def move_shape(self, vector):
        self.vertices += vector

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

    def rotate(self):
        rotation_matrix = np.array([
            [np.cos(self.angle), -np.sin(self.angle)],
            [np.sin(self.angle), np.cos(self.angle)],
        ])

        rotated_vertices = (rotation_matrix @ self.reference_vertices.T).T
        self.vertices = rotated_vertices + self.cm()