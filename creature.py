import random

import pygame


class Creature:
    def __init__(self, x: float, y: float):
        self.creature_pos = pygame.Vector2(x, y)
        self.direction = pygame.Vector2(self.generate_direction()).normalize()
        self.direction_change_timer = random.uniform(2, 5)

        self.radius = 10
        self.speed = 60
        self.creature_color = self.generate_creature_color()

    def change_direction(self):
        self.direction = pygame.Vector2(self.generate_direction()).normalize()
        self.direction_change_timer = random.uniform(2, 5)

    def update(self, dt: float, screen: pygame.Surface):
        self.direction_change_timer = self.direction_change_timer - dt
        if self.direction_change_timer <= 0:
            self.change_direction()
        if (self.creature_pos.x >= screen.get_width() and self.direction.x > 0) or (
            self.creature_pos.x <= 0 and self.direction.x < 0
        ):
            self.direction.x = -self.direction.x
        if (self.creature_pos.y >= screen.get_height() and self.direction.y > 0) or (
            self.creature_pos.y <= 0 and self.direction.y < 0
        ):
            self.direction.y = -self.direction.y

        self.creature_pos += self.direction * self.speed * dt

    def generate_creature_color(self):
        return random.choice(["red", "purple", "blue"])

    def generate_direction(self):

        return random.uniform(-1, 1), random.uniform(-1, 1)

    def draw(self, screen):
        pygame.draw.circle(
            surface=screen,
            color=self.creature_color,
            center=self.creature_pos,
            radius=self.radius,
        )
