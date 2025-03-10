from shape import Shape
from simulation import Simulation

#main-tiedoston käyttö:
#1. Luo Shape-oliot (kulmat tulisi antaa vastapäiväisessä järjestyksessä):
triangle = Shape([[-.5, .5], [-.8, .45], [-.8, .3]],
                 velocity=[1, -1], rotation=3)

square = Shape([[0.8, 0.45], [0.5, 0.5],[0.55, 0.33], [0.8, 0.3]],
                          velocity=[-1, -1], rotation=-2, mass=2)

#1.5 Jos haluat, käytä move_shape() -metodia siirtääksesi kuviota
triangle.move_shape([.1, .3], 1)
square.move_shape([.15, .4], 1)

#2. Luo simulaatiosta olio, johon syötetään Shape-oliot listana
simulation = Simulation([triangle, square], gravity=0)

#3. Kutsu simulaation handle_simulation() -metodia
simulation.handle_simulation()
