"""
core/hud/text.py

Text blocks or data blocks with futuristic fonts, highlight logic, etc.
"""
import pygame
from core.effect import Effect

class TextBlock(Effect):
    def __init__(self, text, x, y, font_path=None, font_size=24, color=(255,255,255)):
        super().__init__()
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        # Load custom font if provided
        if font_path:
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = pygame.font.SysFont("Arial", font_size, bold=False)

    def draw(self, screen):
        text_surf = self.font.render(self.text, True, self.color)
        screen.blit(text_surf, (self.x, self.y))
