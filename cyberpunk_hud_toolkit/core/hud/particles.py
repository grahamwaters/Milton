"""
core/hud/particles.py

Simple particle system for floating shapes or sparkles.
"""
import pygame
import random
import math
from core.effect import Effect

class ParticleEmitter(Effect):
    def __init__(self, x, y, max_particles=100, spawn_rate=5, color=(255,255,255)):
        super().__init__()
        self.x = x
        self.y = y
        self.max_particles = max_particles
        self.spawn_rate = spawn_rate
        self.color = color
        self.particles = []

    def update(self, dt):
        # Spawn new particles
        for _ in range(self.spawn_rate):
            if len(self.particles) < self.max_particles:
                # random velocity
                vx = random.uniform(-30, 30)
                vy = random.uniform(-50, -20)
                life = random.uniform(1, 3)
                size = random.randint(2, 5)
                self.particles.append([self.x, self.y, vx, vy, life, size])

        # Update existing
        for p in self.particles:
            p[0] += p[2]*dt
            p[1] += p[3]*dt
            p[4] -= dt  # life
        # Remove dead
        self.particles = [p for p in self.particles if p[4] > 0]

    def draw(self, screen):
        for p in self.particles:
            x, y, vx, vy, life, size = p
            alpha = int(255 * (life/3))
            col = (*self.color[:3], alpha)
            # quick approach: draw a small rect or circle
            surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, col, (size, size), size)
            screen.blit(surf, (x-size, y-size))
