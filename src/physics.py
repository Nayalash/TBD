# Name: Nayalash Mohammad
# Date: January 20 2020
# File Name: physics.py
# Description: File containing all the basic physics methods

# Slope Method
def calculate_slope(final_y, distance):
    return final_y / distance

# Gravity Collision of Cubes
def canMove(cube, cubes):
    for potCube in cubes:
        if cube.y == potCube.y:
            return False
    return True
