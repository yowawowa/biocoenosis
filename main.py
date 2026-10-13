import random

import pygame

from creature import Creature

pygame.init()

screen = pygame.display.set_mode(size=(800, 600))
clock = pygame.time.Clock()
running = True
dt = 0


creatures = [
    Creature(
        x=random.uniform(0, screen.get_width()),
        y=random.uniform(0, screen.get_height()),
    )
    for _ in range(20)
]

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    bg_color = pygame.Color(114, 239, 168)
    screen.fill(bg_color)

    for creature in creatures:
        creature.update(dt=dt, screen=screen)

    for creature in creatures:
        creature.draw(screen=screen)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
