from config import np, plt, draw_config

# Luokka, johon voi syöttää pisteitä kaksiulotteisena listana,
# sekä vapaavalintaisesti massan, liikenopeusvektorin,
# pyörimisnopeuden (rotation) sekä hitausmomentin.
class Shape:
    def __init__(self, vertices, mass=1, velocity=np.array([0, 0]), rotation=0, j=0.02):
        self.vertices = np.array(vertices)
        self.mass = mass
        self.velocity = np.array(velocity)
        self.rotation = rotation
        self.angle = 0
        self.j = j
        self.reference_vertices = self.cm_in_origin().copy() #Kopio luokan kulmapisteistä, kun sen cm on origossa

    #Metodi, joka palauttaa olion massakeskipisteen
    def cm(self):
        return self.vertices.mean(axis=0)

    #Metodi, joka palauttaa olion reunat, kun massakeskipisteen siirtää origoon.
    def cm_in_origin(self):
        vector_to_origin = np.array([0, 0]) - self.cm()
        return self.vertices + vector_to_origin

    #Metodi, joka liikuttaa oliota vektorin verran per delta_aika (1 = liikutus vektorin verran)
    def move_shape(self, vector, delta_time):
        self.vertices += vector * delta_time
        self.angle += self.rotation * delta_time

    #Olion plottaamismetodi
    def plot(self):
        plt.plot(
            np.append(self.vertices[:, 0], self.vertices[0, 0]),
            np.append(self.vertices[:, 1], self.vertices[0, 1])
        )
        '''
        Debug-piirtokoodi massakeskipisteelle ja kulmien järjestykselle:
        # x, y = self.cm()
        # plt.plot(x, y, "bo")

        # for i in range(len(self.vertices)):
        #     label = chr(65 + i)
        #     plt.text(self.vertices[i, 0], self.vertices[i, 1], label,
        #              fontsize=draw_config["fontsize"],
        #              ha="right", va="bottom", color=draw_config["txt_color"])
        '''

    #Metodi, jolla olion voi piirtää suoraan (sisältää siis plt.show)
    def draw(self):
        plt.figure(figsize=draw_config["figsize"])
        plt.xlim(draw_config["xlim"])
        plt.ylim(draw_config["ylim"])
        self.plot()
        plt.show()

    #Metodi, joka pyörittää olion kulmia päivitetyn anglen mukaiseksi
    #(Käyttää tallennettua reference_verticesiä, jonka cm on origossa, ja lisää muutoksen "oikeisiin" kulmapisteisiin)
    def rotate(self):
        rotation_matrix = np.array([
            [np.cos(self.angle), -np.sin(self.angle)],
            [np.sin(self.angle), np.cos(self.angle)],
        ])

        rotated_vertices = (rotation_matrix @ self.reference_vertices.T).T
        self.vertices = rotated_vertices + self.cm()

    # Metodi, joka palauttaa olion reunat pisteiden syöttämisjärjestyksessä vektoreina
    # Kulmat tulisi siis syöttää oikeassa järjestyksessä, jotta simulaatio toimii oikein
    def get_edges(self):
        edges = []
        for i in range(len(self.vertices)):
            if i == len(self.vertices) - 1:
                edge = self.vertices[0] - self.vertices[i]
            else:
                edge = self.vertices[i + 1] - self.vertices[i]

            edges.append(edge)
        return np.array(edges)
