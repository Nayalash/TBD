import random

from src import physics as p

class Projectile:

    speed = 60

    def __init__(self, x, y, target, distance, color_id):
        self.x = x
        self.y = y
        self.slope = p.calculate_slope(target, distance)
        self.color_id = color_id


    def explode(self):
        print("BOOOM")

    def move(self):
        self.x += Projectile.speed
        self.y += self.slope * Projectile.speed

class ProjectileHolder:

    def __init__(self, color_map_size):
        self.projectiles = []
        self.color_map_size = color_map_size

    def add(self, target, distance, color_id):
        x = 100
        y = 400
        self.projectiles.append(Projectile(x, y, target, distance, color_id))
