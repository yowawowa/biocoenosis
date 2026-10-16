import pygame


class Food:
    def __init__(self, x: float, y: float):
        self.position = pygame.Vector2(x, y)
        self.radius = 5
        self.color = "green"
        self.calories = 20

    def draw(self, screen):
        pygame.draw.circle(
            surface=screen,
            color=self.color,
            center=self.position,
            radius=self.radius,
        )
