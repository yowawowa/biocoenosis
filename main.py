import random

import pygame

from creature import Creature
from food import Food
from hud import HUD

pygame.init()

screen = pygame.display.set_mode(size=(800, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)
running = True
dt = 0


creatures = [
    Creature(
        x=random.uniform(0, screen.get_width()),
        y=random.uniform(0, screen.get_height()),
    )
    for _ in range(10)
]

foods = [
    Food(
        x=random.uniform(0, screen.get_width()),
        y=random.uniform(0, screen.get_height()),
    )
    for _ in range(30)
]

hud = HUD(x=10, y=10)
food_spawn_timer = random.uniform(2, 5)


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                creatures.append(
                    Creature(
                        x=random.uniform(0, screen.get_width()),
                        y=random.uniform(0, screen.get_height()),
                    )
                )
            elif event.key == pygame.K_BACKSPACE and len(creatures) > 0:
                creatures.pop()
            elif event.key == pygame.K_v:
                # TODO vision indicator
                ...

    bg_color = pygame.Color(63, 51, 20)
    screen.fill(bg_color)

    for creature in creatures:
        creature.update(dt=dt, screen=screen, foods=foods)

    creatures = [creature for creature in creatures if creature.is_alive]

    for creature in creatures:
        for food in foods.copy():
            if (
                creature.position.distance_to(food.position)
                <= creature.radius + food.radius
                and creature.is_hungry
            ):
                foods.remove(food)
                creature.eat(food.calories)

    for creature in creatures:
        creature.draw(screen=screen, font=font)

    for food in foods:
        food.draw(screen=screen)

    hud.draw(screen=screen, font=font, items={"Creatures": creatures, "Foods": foods})

    food_spawn_timer -= dt
    if food_spawn_timer <= 0 and len(foods) < 50:
        foods.extend(
            [
                Food(
                    x=random.uniform(0, screen.get_width()),
                    y=random.uniform(0, screen.get_height()),
                ),
                Food(
                    x=random.uniform(0, screen.get_width()),
                    y=random.uniform(0, screen.get_height()),
                ),
                Food(
                    x=random.uniform(0, screen.get_width()),
                    y=random.uniform(0, screen.get_height()),
                ),
            ]
        )
        food_spawn_timer = random.uniform(2, 5)

    dt = clock.tick(60) / 1000
    pygame.display.flip()

pygame.quit()
