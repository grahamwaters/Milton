"""
core/hud/radar.py

A rotating radar sweep effect.
"""
import math
import random
import pygame
from core.effect import Effect

class RadarSweep(Effect):
    def __init__(self, x, y, radius=100, sweep_speed=1.0, color=(0,255,0)):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.angle = 0.0
        self.sweep_speed = sweep_speed  # radians/sec
        self.color = color
        # random "blips"
        self.blips = [(random.uniform(0, 2*math.pi), random.uniform(0, radius)) for _ in range(8)]

    def update(self, dt):
        self.angle += self.sweep_speed * dt
        self.angle %= 2*math.pi

    def draw(self, screen):
        # Draw the outer circle
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 1)
        # Draw some radial lines
        for r in range(0, 360, 45):
            rad = math.radians(r)
            end_x = self.x + math.cos(rad)*self.radius
            end_y = self.y + math.sin(rad)*self.radius
            pygame.draw.line(screen, self.color, (self.x, self.y), (end_x, end_y), 1)

        # Draw blips
        for b_angle, b_dist in self.blips:
            bx = self.x + math.cos(b_angle) * b_dist
            by = self.y + math.sin(b_angle) * b_dist
            pygame.draw.circle(screen, self.color, (int(bx), int(by)), 3)

        # Draw the sweep line
        end_x = self.x + math.cos(self.angle)*self.radius
        end_y = self.y + math.sin(self.angle)*self.radius
        pygame.draw.line(screen, self.color, (self.x, self.y), (end_x, end_y), 2)

        # Possibly draw a translucent sector behind the sweep line for a more
        # advanced scanning effect.
