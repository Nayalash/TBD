# Import Libraries
import pygame
from src import physics as p
from src import cube as c
from src import projectiles as pr
import random

pygame.init()

running = True

dispHeight = 600
dispWidth = 1200

rectHeight = dispHeight - 300
rectWidth = dispWidth / 4

white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
purple = (138, 43, 226)

bg = pygame.image.load("../assets/bg.png")

screen = pygame.display.set_mode((dispWidth, dispHeight))

# Title and Icon
pygame.display.set_caption("Tower Splash")
icon = pygame.image.load('../assets/ts.png')
pygame.display.set_icon(icon)

pygame.draw.rect(screen, blue, (0, 100, 50, 50))
distance = 50
target = -3

slope = p.calculate_slope(target, distance)

x, y = 50, 200
floor = 450

speed = 5

color_map = [
    (255, 255, 255),
    (0, 0, 255),
    (255, 0, 0),
    (0, 255, 0),
    (138, 43, 226)
]

cubeHolder = c.CubeHolder(len(color_map))

pro = pr.ProjectileHolder(len(color_map))

color_id = random.randint(0, len(color_map) - 1)


def gen_color():
    global color_id
    color_id = random.randint(0, len(color_map) - 1)


def draw_rect(surface, fill_color, outline_color, rect, border=1):
    surface.fill(outline_color, rect)
    surface.fill(fill_color, rect.inflate(-border*2, -border*2))

interval = 60
curr_interval = 0

cubeHolder.addCube()

# Main Game Loop
while running:

    screen.blit(bg, (0, 0))

    curr_interval += 1
    if curr_interval >= interval and len(cubeHolder.cubes) <= 4:
        cubeHolder.addCube()
        curr_interval = 0

    # x += speed
    # y += slope * speed
    # pygame.draw.rect(screen, red, (x, y, 30, 30))

    pygame.draw.rect(screen, color_map[color_id], (50, 50, 50, 50))
    for cube in cubeHolder.cubes:
        cubeRect = pygame.Rect(cube.x, cube.y, 103, 95)
        collided = False
        for potCube in cubeHolder.cubes:
            cube_id = cube.id
            if cube_id != potCube.id and cube_id > potCube.id:
                if cubeRect.colliderect(pygame.Rect(potCube.x, potCube.y, 100, 95)):
                    collided = True
                    supposed_diff = 95
                    cube.y -= (cube.y - potCube.y + supposed_diff)
                    cube.force_stationary = True
                    cubeRect = pygame.Rect(cube.x, cube.y, 100, 95)
                    break

        if not cube.force_stationary and cube.y < floor and not collided:
            cube.move()

        draw_rect(screen, color_map[cube.color_id], (0, 0, 0), cubeRect, 3)
        #pygame.draw.rect(screen, color_map[cube.color_id], cubeRect)

    for projectile in pro.projectiles:
        #projRect = pygame.Rect(projectile.x, projectile.y, 30, 30)
        collided = False
        # DO collision checking here TODO
        for cube in cubeHolder.cubes:
            projectileHitBox = pygame.Rect(projectile.x, projectile.y, 20, 20)
            if projectileHitBox.colliderect(pygame.Rect(cube.x, cube.y, 100, 95)):
                if projectile.color_id == cube.color_id:
                    # collision here
                    cubeHolder.cubes.remove(cube)
                    pro.projectiles.remove(projectile)

                    for c in cubeHolder.cubes:
                        c.force_stationary = False

        # collision check end
        pygame.draw.circle(screen, color_map[projectile.color_id], (int(projectile.x), int(projectile.y)), 20)
        projectile.move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            target = y - 400
            pro.add(target, 1000, color_id)
            gen_color()

    pygame.display.update()
