import random

class Cube:

    id_base = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hit = False
        self.on_surface = False
        self.gravity = 0.01
        self.fall_speed = 0
        self.id = Cube.id_base
        Cube.id_base += 1

    def move(self):
        if not self.on_surface:
            self.fall_speed += 2.3
            self.y += self.fall_speed

    def is_touching(self, cube):
        is_y = self.y >= cube.y >= (self.y - 95)
        is_x = self.x >= cube.x >= (self.x - 100)


class CubeHolder:

    def __init__(self):
        self.cubes = []
        self.posModifier = 100

    def addCube(self):
        lastIndex = len(self.cubes)
        self.cubes.append(Cube(1000, 200 + self.posModifier * lastIndex))
