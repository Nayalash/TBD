# Name: Nayalash Mohammad
# Date: January 20 2020
# File Name: projectiles.py
# Description: File containing projectile object

import random

import physics as p

# Create Projectile Object

class Projectile:
    # Define Base Speed
    speed = 60

    # Default Constructor
    def __init__(self, x, y, target, distance, color_id):
        self.x = x
        self.y = y
        self.slope = p.calculate_slope(target, distance)
        self.color_id = color_id

    # On Hit
    def explode(self):
        print("BOOOM")

    # Move Projectile to Target Point
    def move(self):
        self.x += Projectile.speed
        self.y += self.slope * Projectile.speed

# Projectile Holder Object
class ProjectileHolder:

    # Define Method to Hold Projectiles
    def __init__(self, color_map_size):
        self.projectiles = []
        self.color_map_size = color_map_size

    # Store Projectiles and Add
    def add(self, target, distance, color_id):
        x = 100
        y = 400
        self.projectiles.append(Projectile(x, y, target, distance, color_id))
