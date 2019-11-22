import pygame
from src import physics as p

pygame.init()

running = True
dispHeight = 750
dispWidth = 1400

rectHeight = dispHeight - 300
rectWidth = dispWidth/4

white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
purple = (138,43,226)

screen = pygame.display.set_mode((dispWidth, dispHeight))


# Title and Icon
pygame.display.set_caption("Title Here")
# icon = pygame.image.load('Insert Image Path')
# pygame.display.set_icon(icon)


pygame.draw.rect(screen, blue,(0, 100, 50, 50))
distance = 50
target = -3

slope = p.calculate_slope(target, distance)

x, y = 50, 200

speed = 5

# Main Game Loop
while running:
        x += speed
        y += slope * speed
        pygame.draw.rect(screen, red, (x, y, 30, 30))
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False

        pygame.display.update()

