from config import np, plt

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