def calculate_slope(final_y, distance):
    return final_y / distance


def canMove(cube, cubes):
    for potCube in cubes:
        if cube.y == potCube.y:
            return False
    return True