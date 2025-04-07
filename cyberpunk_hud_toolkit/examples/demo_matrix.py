#!/usr/bin/env python3
"""
demo_matrix.py

A rough approximation of 'Matrix rain' effect with PyGame
and the same scene/effect architecture.
"""

import pygame
import random
import time

from core.engine import Engine
from core.scene import Scene
from core.effect import Effect

class MatrixColumn:
    def __init__(self, x, screen_height, speed=100):
        self.x = x
        self.y = random.randint(-screen_height, 0)
        self.speed = speed
        self.chars = []
        self.screen_height = screen_height
        # generate random length
        self.length = random.randint(10, 30)

    def update(self, dt):
        self.y += self.speed * dt
        if self.y > self.screen_height + self.length*20:
            self.y = random.randint(-self.screen_height, 0)
            self.length = random.randint(10, 30)
            self.chars = []

    def draw(self, screen, font):
        # each 'cell' is about 20px
        if not self.chars or len(self.chars) < self.length:
            self.chars = [chr(random.randint(33, 126)) for _ in range(self.length)]
        # topmost char is bright
        offset_y = 0
        for i, ch in enumerate(self.chars):
            color = (0,255,0) if i == (len(self.chars)-1) else (0,180,0)
            rendered = font.render(ch, True, color)
            screen.blit(rendered, (self.x, self.y + offset_y))
            offset_y -= 20  # upward

class MatrixEffect(Effect):
    def __init__(self, width, height, columns=40):
        super().__init__()
        self.width = width
        self.height = height
        self.columns = columns
        self.column_objs = []
        self.font = None

    def reset(self):
        self.font = pygame.font.SysFont("Courier", 20, bold=True)
        step = self.width // self.columns
        self.column_objs = [MatrixColumn(x, self.height, speed=random.randint(80,180))
                            for x in range(0, self.width, step)]

    def update(self, dt):
        for col in self.column_objs:
            col.update(dt)

    def draw(self, screen):
        # black background
        screen.fill((0,0,0))
        for col in self.column_objs:
            col.draw(screen, self.font)

def main():
    engine = Engine(width=800, height=600, title="Matrix Rain")
    scene = Scene(effects=[MatrixEffect(800,600,columns=30)], duration=10.0)
    engine.add_scene(scene)
    engine.run()

if __name__ == "__main__":
    main()
