# Name: Nayalash Mohammad
# Date: January 20 2020
# File Name: cube.py
# Description: File containing cube object

import random

# Create Cube Object
class Cube:

    id_base = 1

    # Constructor For Cube Properties
    def __init__(self, x, y, color_map_size):
        self.x = x
        self.y = y
        self.hit = False
        self.on_surface = False
        self.gravity = 0.01
        self.fall_speed = 0
        self.id = Cube.id_base
        Cube.id_base += 1
        # Color Generation
        self.color_id = random.randint(0, color_map_size - 1)
        self.force_stationary = False

    # Cube Falling
    def move(self):
        if not self.on_surface:
            self.fall_speed += 2.3
            self.y += self.fall_speed

    # Cube Stacking
    def is_touching(self, cube):
        is_y = self.y >= cube.y >= (self.y - 95)
        is_x = self.x >= cube.x >= (self.x - 100)
        return is_y and is_x

# Create Cube Holder Object
class CubeHolder:

    # Constructor with Cube Holder Properties
    def __init__(self, color_map_size):
        self.cubes = []
        self.posModifier = 100
        self.color_map_size = color_map_size

    # Hold Cubes in Array
    def addCube(self):
        self.cubes.append(Cube(1000, 0, self.color_map_size))
