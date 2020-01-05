# Import Libraries
import pygame
from src import physics as p
from src import cube as c
from src import projectiles as pr
import random
import time

pygame.init()

running = True

dispHeight = 600
dispWidth = 1200

white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
purple = (138, 43, 226)

font = pygame.font.SysFont("monospace", 64)

bg = pygame.image.load("../assets/bg.png")

shooter = pygame.image.load("../assets/shooter.png")
pointer = pygame.image.load("../assets/pointer.png")
over = pygame.image.load("../assets/over.png")
gnd = pygame.image.load("../assets/gnd.png")
start = pygame.image.load("../assets/start.png")
help = pygame.image.load("../assets/help.png")
quit = pygame.image.load("../assets/quit.png")
rank = pygame.image.load("../assets/rank.png")
shop = pygame.image.load("../assets/shop.png")
back = pygame.image.load("../assets/back.png")
helpD = pygame.image.load("../assets/helpD.png")
shopD = pygame.image.load("../assets/shopD.png")

bullet_sound = pygame.mixer.Sound('../assets/bullet.wav')
button = pygame.mixer.Sound('../assets/button.wav')
music = pygame.mixer.music.load('../assets/music.mp3')


pygame.mixer.music.play(-1)

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
score = 0

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
    surface.fill(fill_color, rect.inflate(-border * 2, -border * 2))


interval = 60
curr_interval = 0
game_over = False
game_over_phase = False
game_over_ticks = 45
curr_game_over_ticks = 0
none_left = False
game_restarted = False

in_game = False
in_help = False
in_shop = False
in_rank = False


def reset():
    cubeHolder.cubes.clear()
    c.id_base = 1
    pro.projectiles.clear()
    global score
    score = 0

cubeHolder.addCube()

# Main Game Loop
while running:

    if in_game:
        if len(cubeHolder.cubes) > 4:
            game_over_phase = True

        if game_over_phase:
            curr_game_over_ticks += 1

        if curr_game_over_ticks > game_over_ticks:
            reset()
            curr_game_over_ticks = 0
            game_over_phase = False
            game_over = True

        if game_over:
            screen.fill(white)
            screen.blit(over, (400, 200))
        else:

            screen.blit(bg, (0, 0))
            screen.blit(gnd, (0, 580))
            scoreText = font.render("SCORE: " + str(score), 1, (0, 0, 0))
            screen.blit(scoreText, (10, 130))

            curr_interval += 1
            if curr_interval >= interval and len(cubeHolder.cubes) <= 5:
                cubeHolder.addCube()
                curr_interval = 0
                none_left = False
                game_restarted = False

            if len(cubeHolder.cubes) == 0 and not none_left and not game_restarted:
                none_left = True
                score += 2

            screen.blit(pointer, (10, 10))
            screen.blit(back, (10, 200))

            pygame.draw.rect(screen, color_map[color_id], (220, 20, 50, 50))

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

            for projectile in pro.projectiles:
                collided = False
                for cube in cubeHolder.cubes:
                    projectileHitBox = pygame.Rect(projectile.x, projectile.y, 20, 20)
                    if projectileHitBox.colliderect(pygame.Rect(cube.x, cube.y, 100, 95)) and not game_over_phase:
                        if projectile.color_id == cube.color_id:
                            # collision here
                            score += 1

                            cubeHolder.cubes.remove(cube)
                            pro.projectiles.remove(projectile)

                        if projectile.color_id != cube.color_id:
                            score -= 1

                            for c in cubeHolder.cubes:
                                c.force_stationary = False

                # collision check end
                pygame.draw.circle(screen, color_map[projectile.color_id], (int(projectile.x), int(projectile.y)), 20)
                projectile.move()

            screen.blit(shooter, (65, 380))
    else:
        if in_shop:
            screen.blit(bg, (0, 0))
            screen.blit(back, (10, 480))
            screen.blit(shopD, (365,20))

        elif in_help:
            screen.blit(bg, (0, 0))
            screen.blit(back, (10, 480))
            screen.blit(helpD, (220,20))
        elif in_rank:
            screen.blit(bg, (0, 0))
            screen.blit(back, (10, 480))
            scoreText = font.render("TOP SCORE: " + str(score), 1, (0, 0, 0))
            screen.blit(scoreText, (440, 240))
        else:
            screen.blit(bg, (0, 0))
            screen.blit(start, (440, 20))
            screen.blit(shop, (440, 130))
            screen.blit(rank, (440, 240))
            screen.blit(help, (440, 350))
            screen.blit(quit, (440, 460))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                button.play()
                time.sleep(0.5)
                running = False
            if event.key == pygame.K_r and in_game and game_over:
                button.play()
                game_over = False
                game_restarted = True
            elif event.key == pygame.K_s and not in_game and not in_shop and not in_help:
                button.play()
                in_game = True
            elif event.key == pygame.K_5 and in_shop:
                button.play()
                bg = pygame.image.load("../assets/bg1.jpg")
            elif event.key == pygame.K_6 and in_shop:
                button.play()
                bg = pygame.image.load("../assets/bg2.jpg")
            elif event.key == pygame.K_h and not in_game:
                button.play()
                in_help = True
            elif event.key == pygame.K_g and not in_game and not in_shop and not in_help:
                button.play()
                in_rank = True
            elif event.key == pygame.K_b and not in_game and not in_help:
                button.play()
                in_shop = True
            elif event.key == pygame.K_1 and (in_game or in_help or in_shop or in_rank):
                button.play()
                if in_game:
                    reset()
                    game_restarted = True
                in_help, in_rank, in_shop, in_game = False, False, False, False

        if event.type == pygame.MOUSEBUTTONUP and not game_over and not game_over_phase:
            x, y = pygame.mouse.get_pos()
            target = y - 400
            pro.add(target, 1000, color_id)
            gen_color()

    pygame.display.update()
