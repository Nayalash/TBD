# Import Libraries
import pygame
from src import physics as p
from src import cube as c

pygame.init()

running = True

dispHeight = 750
dispWidth = 1400

rectHeight = dispHeight - 300
rectWidth = dispWidth / 4

white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
purple = (138, 43, 226)

screen = pygame.display.set_mode((dispWidth, dispHeight))

# Title and Icon
pygame.display.set_caption("Tower Splash")
# icon = pygame.image.load('Insert Image Path')
# pygame.display.set_icon(icon)


pygame.draw.rect(screen, blue, (0, 100, 50, 50))
distance = 50
target = -3

slope = p.calculate_slope(target, distance)

x, y = 50, 200
floor = 600

speed = 5
cubeHolder = c.CubeHolder()

# Main Game Loop
while running:
    if len(cubeHolder.cubes) < 5:
        cubeHolder.addCube()

    screen.fill((0, 0, 0))
    x += speed
    y += slope * speed
    pygame.draw.rect(screen, red, (x, y, 30, 30))


    for cube in cubeHolder.cubes:
        cubeRect = pygame.Rect(cube.x, cube.y, 100, 95)
        collided = False
        for potCube in cubeHolder.cubes:
            cube_id = cube.id
            if cube_id != potCube.id and cube_id < potCube.id:
                if cubeRect.colliderect(pygame.Rect(potCube.x, potCube.y, 100, 95)):
                    print('touch! ' + str(cube_id + potCube.id))
                    collided = True
                    break

        if cube.y < floor and not collided:
            cube.move()

        pygame.draw.rect(screen, blue, cubeRect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

