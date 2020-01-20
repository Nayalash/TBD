# Name: Nayalash Mohammad
# Date: January 20 2020
# File Name: physics.py
# Description: File containing all the basic physics methods

# Import libraries and other files
import pygame
import physics as p
import cube as c
import projectiles as pr
import random
import scoreSaver as s
import sys

pygame.init() # Initialize PyGame

# Define Global Variable for the running of the Main Game Loop
running = True

# Set Constant Screen Dimensions
dispHeight = 600
dispWidth = 1200

# Define global RGB values for colors being used
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
purple = (138, 43, 226)

# Set System-Wide Font and FontSize
font = pygame.font.SysFont("monospace", 64)

# Load Image Files
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

# Load Audio Files
bullet_sound = pygame.mixer.Sound('../assets/bullet.wav')
button = pygame.mixer.Sound('../assets/button.wav')
music = pygame.mixer.music.load('../assets/music.mp3')

# Play Background Music Forever
pygame.mixer.music.play(-1)

# Create Pygame Screen
screen = pygame.display.set_mode((dispWidth, dispHeight))

# Title and Icon
pygame.display.set_caption("Tower Splash")
icon = pygame.image.load('../assets/ts.png')
pygame.display.set_icon(icon)

pygame.draw.rect(screen, blue, (0, 100, 50, 50))

# Define Target Variables
distance = 50
target = -3

# Call Slope Method
slope = p.calculate_slope(target, distance)

# Projectile Global Configs
x, y = 50, 200
floor = 450
speed = 5

# Main Score Calculator
score = 0

# Create map of colors for the falling cubes
color_map = [

    (255, 255, 255),
    (0, 0, 255),
    (255, 0, 0),
    (0, 255, 0),
    (138, 43, 226)
]

# Create CubeHolder Object
cubeHolder = c.CubeHolder(len(color_map))

# Create Projectile Holder Object
pro = pr.ProjectileHolder(len(color_map))

# Generate Random Colors
color_id = random.randint(0, len(color_map) - 1)


# Method to Generate a Color
def gen_color():
    global color_id
    color_id = random.randint(0, len(color_map) - 1)

# Method to draw a bolded cube, instead of linear
def draw_rect(surface, fill_color, outline_color, rect, border=1):
    surface.fill(outline_color, rect)
    surface.fill(fill_color, rect.inflate(-border * 2, -border * 2))


# Define Variables for Reset Functionality
interval = 60
curr_interval = 0
game_over = False
game_over_phase = False
game_over_ticks = 45
curr_game_over_ticks = 0
none_left = False
game_restarted = False

# Define Booleans for Screen Navigation
in_game = False
in_help = False
in_shop = False
in_rank = False

# Define Reset Option
def reset():
    cubeHolder.cubes.clear()
    c.id_base = 1
    pro.projectiles.clear()
    global score
    score = 0

# Add The First Cube
cubeHolder.addCube()

# Main Game Loop
while running:

    # Define Screens
    if in_game:

        # Stop Game after certain Block Count
        if len(cubeHolder.cubes) > 4:
            game_over_phase = True

        # FPS Alignment
        if game_over_phase:
            curr_game_over_ticks += 1

        # Game Over and Score Setter
        if curr_game_over_ticks > game_over_ticks:
            if(s.isHighScore(score)):
                s.setHighScore(score)
            reset()
            curr_game_over_ticks = 0
            game_over_phase = False
            game_over = True

        # Add Game Over Screen
        if game_over:
            screen.fill(white)
            screen.blit(over, (400, 200))

        # Main Game Screen
        else:
            # Render Main Assets
            screen.blit(bg, (0, 0))
            screen.blit(gnd, (0, 580))

            # Score Setup
            scoreText = font.render("SCORE: " + str(score), 1, (0, 0, 0))
            screen.blit(scoreText, (10, 130))

            # FPS Alignment
            curr_interval += 1

            # Actions after Certain Block Counts
            if curr_interval >= interval and len(cubeHolder.cubes) <= 5:
                cubeHolder.addCube()
                curr_interval = 0
                none_left = False
                game_restarted = False

            # Condition when all Cubes are finished
            if len(cubeHolder.cubes) == 0 and not none_left and not game_restarted:
                none_left = True
                score += 2

            # Render Secondary Assets
            screen.blit(pointer, (10, 10))
            screen.blit(back, (10, 200))

            # Next Ball Color Rect
            pygame.draw.rect(screen, color_map[color_id], (220, 20, 50, 50))

            # Collision Checking of Cubes
            for cube in cubeHolder.cubes:
                cubeRect = pygame.Rect(cube.x, cube.y, 103, 95)
                collided = False

                # Stack Checking
                for potCube in cubeHolder.cubes:
                    cube_id = cube.id
                    # Collision with top Rectangle
                    if cube_id != potCube.id and cube_id > potCube.id:
                        # Collision with bottom Rectangle
                        if cubeRect.colliderect(pygame.Rect(potCube.x, potCube.y, 100, 95)):
                            collided = True
                            # Activate Gravity
                            supposed_diff = 95
                            cube.y -= (cube.y - potCube.y + supposed_diff)
                            cube.force_stationary = True
                            cubeRect = pygame.Rect(cube.x, cube.y, 100, 95)
                            break

                # Cube Falling Physics
                if not cube.force_stationary and cube.y < floor and not collided:
                    cube.move()

                # Addition of Cubes
                draw_rect(screen, color_map[cube.color_id], (0, 0, 0), cubeRect, 3)

            # Collision Checking of Projectiles
            for projectile in pro.projectiles:
                collided = False
                # Collision with Cubes
                for cube in cubeHolder.cubes:
                    # Generate Hit Area
                    projectileHitBox = pygame.Rect(projectile.x, projectile.y, 20, 20)
                    # Check For a Hit
                    if projectileHitBox.colliderect(pygame.Rect(cube.x, cube.y, 100, 95)) and not game_over_phase:
                        # Action
                        if projectile.color_id == cube.color_id:
                            # Increment score on contact with projectiles
                            score += 1
                            cubeHolder.cubes.remove(cube)
                            pro.projectiles.remove(projectile)

                        # Decrease Score when Wrong Hit
                        if projectile.color_id != cube.color_id:
                            score -= 1

                        for c in cubeHolder.cubes:
                            c.force_stationary = False

                # Projectile Motion Config
                pygame.draw.circle(screen, color_map[projectile.color_id], (int(projectile.x), int(projectile.y)), 20)
                projectile.move()

            # Render Shooter Assets
            screen.blit(shooter, (65, 380))

    else:
        # Set Game Screens
        if in_shop:
            screen.blit(bg, (0, 0))
            screen.blit(back, (10, 480))
            screen.blit(shopD, (365,20))
        # Set Help Screen
        elif in_help:
            screen.blit(bg, (0, 0))
            screen.blit(back, (10, 480))
            screen.blit(helpD, (220,20))
        # Set Rank Screen
        elif in_rank:
            screen.blit(bg, (0, 0))
            screen.blit(back, (10, 480))
            scoreText = font.render("TOP SCORE: " + str(s.getScore()), 1, (0, 0, 0))
            screen.blit(scoreText, (440, 240))
        # Set Home Screen
        else:
            screen.blit(bg, (0, 0))
            screen.blit(start, (440, 20))
            screen.blit(shop, (440, 130))
            screen.blit(rank, (440, 240))
            screen.blit(help, (440, 350))
            screen.blit(quit, (440, 460))

    # Event Handling
    for event in pygame.event.get():
        # Quit Game
        if event.type == pygame.QUIT:
            running = False
        # Set Up Key Presses
        if event.type == pygame.KEYUP:

            # Quit
            if event.key == pygame.K_q:
                button.play()
                exit()
                running = False
                sys.exit()
            # Reset
            if event.key == pygame.K_r and in_game and game_over:
                button.play()
                game_over = False
                game_restarted = True
            # Start
            elif event.key == pygame.K_s and not in_game and not in_shop and not in_help:
                button.play()
                in_game = True
            # Shop Selectors
            elif event.key == pygame.K_5 and in_shop:
                button.play()
                bg = pygame.image.load("../assets/bg1.jpg")
            elif event.key == pygame.K_6 and in_shop:
                button.play()
                bg = pygame.image.load("../assets/bg2.jpg")
            # Help
            elif event.key == pygame.K_h and not in_game:
                button.play()
                in_help = True
            # LeaderBoard
            elif event.key == pygame.K_g and not in_game and not in_shop and not in_help:
                button.play()
                in_rank = True
            # Shop
            elif event.key == pygame.K_b and not in_game and not in_help:
                button.play()
                in_shop = True
            # Back To Home
            elif event.key == pygame.K_1 and (in_game or in_help or in_shop or in_rank):
                button.play()
                if in_game:
                    reset()
                    game_restarted = True
                in_help, in_rank, in_shop, in_game = False, False, False, False

        # Projectile Event Handling
        if event.type == pygame.MOUSEBUTTONUP and not game_over and not game_over_phase:
            bullet_sound.play()
            x, y = pygame.mouse.get_pos()
            target = y - 400
            pro.add(target, 1000, color_id)
            gen_color()

    pygame.display.update() # Update Screen
