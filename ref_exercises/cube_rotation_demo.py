import time
import math
import random
import framebuf
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
from fifo import Fifo

led_pin = machine.Pin(25, machine.Pin.OUT)
button1 = Pin(9, Pin.IN, Pin.PULL_UP)
button2 = Pin(7, Pin.IN, Pin.PULL_UP)
button3 = Pin(8, Pin.IN, Pin.PULL_UP)

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)
oled.fill(0)

verts = [
    [-10, -10, -10],
    [10, -10, -10],
    [10, 10, -10],
    [-10, 10, -10],
    [-10, -10, 10],
    [10, -10, 10],
    [10, 10, 10],
    [-10, 10, 10]
]

edges = [
    [0, 1], [1, 2], [2, 3], [3, 0],
    [4, 5], [5, 6], [6, 7], [7, 4],
    [0, 4], [1, 5], [2, 6], [3, 7]
]


# verts = [
# [0, 10, -10], [-10, 10, 0], [10, -10, 0]
# ]

# edges = [
# [0, 1], [1, 2], [2, 0],
# ]


class Button:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)

    def press(self):
        if not self.pin.value():
            return True
        else:
            return False


class Encoder:
    def __init__(self, rot_a, rot_b):
        self.a = Pin(rot_a, mode=Pin.IN, pull=Pin.PULL_UP)
        self.b = Pin(rot_b, mode=Pin.IN, pull=Pin.PULL_UP)
        self.fifo = Fifo(30, typecode='i')
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)
        self.modifier = 1
        self.last_modifier = 1

    def handler(self, pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)


class Object:

    def __init__(self, x_offset, y_offset, direction, verts=[], edges=[]):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.verts = verts
        self.edges = edges
        self.direction = direction

    def move(self, x, y):
        for vertex in self.verts:
            vertex[0] += x
            vertex[1] += y

    def rotate_x(self, angle):
        rotated_verts = []
        for vert in self.verts:
            y = vert[1] * math.cos(self.direction * angle) - vert[2] * math.sin(self.direction * angle)
            z = vert[1] * math.sin(self.direction * angle) + vert[2] * math.cos(self.direction * angle)
            rotated_verts.append([vert[0], y, z])
        self.verts = rotated_verts

    def rotate_y(self, angle):
        rotated_verts = []
        for vert in self.verts:
            x = vert[0] * math.cos(self.direction * angle) - vert[2] * math.sin(self.direction * angle)
            z = vert[0] * math.sin(self.direction * angle) + vert[2] * math.cos(self.direction * angle)
            rotated_verts.append([x, vert[1], z])
        self.verts = rotated_verts

    def rotate_z(self, angle):
        rotated_verts = []
        for vert in self.verts:
            x = vert[0] * math.cos(self.direction * angle) - vert[1] * math.sin(self.direction * angle)
            y = vert[0] * math.sin(self.direction * angle) + vert[1] * math.cos(self.direction * angle)
            rotated_verts.append([x, y, vert[2]])
        self.verts = rotated_verts

    def draw(self):
        oled.fill(0)
        for edge in edges:
            start = self.verts[edge[0]]
            end = self.verts[edge[1]]

            x1 = int(start[0] * 2) + 64
            y1 = int(start[1] * 2) + 32
            x2 = int(end[0] * 2) + 64
            y2 = int(end[1] * 2) + 32
            oled.line(x1, y1, x2, y2, 1)

        oled.show()


cube = Object(0, 0, 1, verts, edges)
rot = Encoder(10, 11)
button1 = Button(9)
button2 = Button(7)
button3 = Button(8)

an_x = 1
an_y = 1
an_z = 1
speed = .1
while True:
    oled.invert(0)
    cube.rotate_z(0.01)
    cube.rotate_x(0.002)
    if rot.fifo.has_data():
        rot.modifier = rot.fifo.get()
        print(str(rot.modifier))

    if rot.modifier != rot.last_modifier:
        oled.fill(0)
        if rot.modifier == 1:

            oled.text("1", 0, 8)

        elif rot.modifier == -1:
            oled.text("-1", 0, 8)

        oled.show()
        rot.last_modifier = rot.modifier
        time.sleep(0.1)

    an_zs = an_z * speed
    an_xs = an_x * speed
    an_ys = an_y * speed

    if button1.press():
        if rot.modifier == -1:
            cube.rotate_z(an_zs)
        elif rot.modifier == 1:
            cube.move(1, 0)

    if button2.press():
        if rot.modifier == -1:
            cube.rotate_x(an_xs)
        elif rot.modifier == 1:
            cube.move(-1, 0)
    if button3.press():
        if rot.modifier == -1:

            if cube.direction == 1:
                cube.direction = -1
            else:
                cube.direction = 1
        elif rot.modifier == 1:
            cube.rotate_z(an_zs)

    cube.draw()

    time.sleep(0.005)

