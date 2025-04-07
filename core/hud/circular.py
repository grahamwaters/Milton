"""
core/hud/circular.py

A Circular progress meter or gauge, with an optional glow effect.
"""
import math
import pygame
from core.effect import Effect

class CircularProgress(Effect):
    def __init__(self, x, y, radius=50, value=0.0, color=(0,255,255), bg_color=(50,50,50), thickness=8):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.value = value  # 0..1
        self.color = color
        self.bg_color = bg_color
        self.thickness = thickness
        self.speed = 0.0  # if you want to animate the value

    def update(self, dt):
        # Example: if you wanted to animate the value
        self.value += self.speed * dt
        self.value = max(0.0, min(1.0, self.value))

    def draw(self, screen):
        # Draw background ring
        pygame.draw.circle(screen, self.bg_color, (self.x, self.y), self.radius, self.thickness)

        # Draw progress arc
        start_angle = -math.pi / 2
        end_angle = start_angle + 2*math.pi * self.value
        rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)
        pygame.draw.arc(screen, self.color, rect, start_angle, end_angle, self.thickness)

        # Optionally add a glow effect
        # e.g. draw a bigger circle with alpha
        # (leaving it out for brevity)
