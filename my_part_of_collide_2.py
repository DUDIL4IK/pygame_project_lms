#number2
import pygame
import sys
import math

pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("НУ ТИПО ОТСКОК")

white = (255, 255, 255)
black = (0, 0, 0)

circles = []

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            circle_data = [x, y, 10, 45, 100]
            circles.append(circle_data)

    screen.fill(white)

    for circle_data in circles:
        x, y, radius, angle, speed = circle_data

        x += speed * math.cos(math.radians(angle)) * clock.get_time() / 1000
        y -= speed * math.sin(math.radians(angle)) * clock.get_time() / 1000

        if x - radius < 0 or x + radius > window_size[0]:
            angle = 180 - angle
        if y - radius < 0 or y + radius > window_size[1]:
            angle = -angle

        pygame.draw.circle(screen, black, (int(x), int(y)), radius)

        circle_data[0] = x
        circle_data[1] = y
        circle_data[3] = angle

    pygame.display.flip()

    clock.tick(60)
