import pygame


class HUD:
    def __init__(self, x: float, y: float):
        self.position = pygame.Vector2(x, y)

    def draw(
        self,
        screen: pygame.Surface,
        font: pygame.font.Font,
        items: dict[str, list],
    ):
        offset_y = 0
        for name, spisok in items.items():
            hud_text = font.render(f"{name} {len(spisok)}", True, "white")
            text_rect = hud_text.get_rect(
                topleft=(self.position.x, self.position.y + offset_y)
            )

            screen.blit(hud_text, text_rect)
            offset_y += font.get_linesize()
