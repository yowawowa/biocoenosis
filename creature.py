import random

import pygame

from food import Food


class Creature:
    def __init__(self, x: float, y: float):
        self.position = pygame.Vector2(x, y)
        self.direction = pygame.Vector2(self.generate_direction()).normalize()
        self.direction_change_timer = random.uniform(2, 5)

        self.radius = 10
        self.speed = 60
        self.color = self._generate_creature_color()

        self.energy = 100
        self.is_alive = True

        self.nearest_food = None
        self.vision_radius = 70

    @property
    def is_hungry(self) -> bool:
        return self.energy <= 70

    def change_direction(self):
        self.direction = pygame.Vector2(self.generate_direction()).normalize()
        self.direction_change_timer = random.uniform(2, 5)

    # TODO func too big :()
    def update(self, dt: float, screen: pygame.Surface, foods: list[Food]):
        # looking for closest food withing vision limit
        self.nearest_food = None
        if self.is_hungry:
            min_distance = float("inf")
            for food in foods:
                cur_pos = self.position.distance_to(food.position)
                if cur_pos < min_distance and cur_pos <= self.vision_radius:
                    min_distance = cur_pos
                    self.nearest_food = food

        # changing direction to closest food
        if self.nearest_food is not None:
            new_direction = self.nearest_food.position - self.position
            if new_direction.length_squared() > 0:
                self.direction = new_direction.normalize()

        # energy depletion on every frame and death if 0
        self.energy -= 1 * dt
        if self.energy <= 0:
            self.is_alive = False
            return
        # if no food random direction change timer is progressing and direction changes on end
        if self.nearest_food is None:
            self.direction_change_timer -= dt
            if self.direction_change_timer <= 0:
                self.change_direction()

        # screen border collision detection, overlap is intended for feeling of outside world being bigger that screen
        if (self.position.x >= screen.get_width() and self.direction.x > 0) or (
            self.position.x <= 0 and self.direction.x < 0
        ):
            self.direction.x = -self.direction.x
        if (self.position.y >= screen.get_height() and self.direction.y > 0) or (
            self.position.y <= 0 and self.direction.y < 0
        ):
            self.direction.y = -self.direction.y

        # movement
        self.position += self.direction * self.speed * dt

    def eat(self, calories):
        self.energy = min(self.energy + calories, 100)

    def _generate_creature_color(self):
        # RGBA
        return [
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            255,
        ]

    def generate_direction(self):
        return random.uniform(-1, 1), random.uniform(-1, 1)

    @property
    def energy_color(self):
        if self.energy < 30:
            return "red"
        elif self.energy < 60:
            return "yellow"
        else:
            return "green"

    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        energy_text = font.render(str(int(self.energy)), True, self.energy_color)
        pygame.draw.circle(
            surface=screen,
            color=self.color,
            center=self.position,
            radius=self.radius,
        )
        pygame.draw.circle(
            screen,
            "gray",
            self.position,
            self.vision_radius,
            width=1,
        )
        text_rect = energy_text.get_rect(
            center=(self.position.x, self.position.y - self.radius - 10)
        )
        screen.blit(energy_text, text_rect)
