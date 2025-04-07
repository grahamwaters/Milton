#!/usr/bin/env python3
"""
demo_fireworks.py

A dynamic fireworks show. Each firework:
  - rises from bottom
  - explodes into colorful sparks
  - sparks fade out
We also draw a starry background, either from a static image or generated stars.

Requires:
 - assets/images/starry_sky.png (optional background)
 - or we generate random stars if that file is not found
"""

import pygame
import random
import os
import math

from core.engine import Engine
from core.scene import Scene
from core.effect import Effect

class StarryBackground(Effect):
    """
    Renders a starry night background, either from an image or random points.
    """
    def __init__(self, image_path=None, star_count=100):
        super().__init__()
        self.image_path = image_path
        self.star_count = star_count
        self._bg_image = None
        self._stars = []

    def reset(self):
        super().reset()
        if self.image_path and os.path.exists(self.image_path):
            self._bg_image = pygame.image.load(self.image_path).convert()
        else:
            self._bg_image = None
            # generate random stars
            width, height = pygame.display.get_surface().get_size()
            self._stars = []
            for _ in range(self.star_count):
                x = random.randint(0, width)
                y = random.randint(0, height)
                brightness = random.randint(128,255)
                self._stars.append((x,y,brightness))

    def draw(self, screen):
        if not self.is_active:
            return
        if self._bg_image:
            screen.blit(self._bg_image, (0,0))
        else:
            # fill black
            screen.fill((0,0,0))
            # draw stars
            for (sx, sy, br) in self._stars:
                screen.set_at((sx, sy), (br, br, br))

class FireworkEffect(Effect):
    """
    A single firework that rises and then explodes into sparks.
    """
    def __init__(self, x, ground_y, color, spark_count=50):
        super().__init__()
        self.x = x
        self.ground_y = ground_y
        self.color = color
        self.spark_count = spark_count

        # initial
        self.y = ground_y
        self.state = "ascending"  # ascending -> exploded
        self.vy = random.uniform(-300, -200)  # speed upward
        self.sparks = []

    def update(self, dt):
        super().update(dt)
        if not self.is_active:
            return

        if self.state == "ascending":
            self.y += self.vy * dt
            # gravity
            self.vy += 150 * dt
            if self.vy >= 0:
                # reached apex
                self.state = "exploded"
                self._create_sparks()
        else:
            # update sparks
            for s in self.sparks:
                s["x"] += s["vx"] * dt
                s["y"] += s["vy"] * dt
                s["vy"] += 150 * dt  # gravity
                s["life"] -= dt

            # remove dead sparks
            self.sparks = [s for s in self.sparks if s["life"] > 0]
            if not self.sparks:
                # no sparks left, kill this effect
                self.kill()

    def draw(self, screen):
        if not self.is_active:
            return
        if self.state == "ascending":
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)
        else:
            # draw sparks
            for s in self.sparks:
                alpha = int(255 * (s["life"] / s["max_life"]))
                col = (*self.color[:3], alpha)
                spark_surf = pygame.Surface((4,4), pygame.SRCALPHA)
                pygame.draw.circle(spark_surf, col, (2,2), 2)
                screen.blit(spark_surf, (s["x"]-2, s["y"]-2))

    def _create_sparks(self):
        for _ in range(self.spark_count):
            angle = random.uniform(0, 2*math.pi)
            speed = random.uniform(50, 200)
            vx = math.cos(angle)*speed
            vy = math.sin(angle)*speed
            life = random.uniform(1,2)
            self.sparks.append({
                "x": self.x,
                "y": self.y,
                "vx": vx,
                "vy": vy,
                "life": life,
                "max_life": life
            })

class FireworksManager(Effect):
    """
    Spawns multiple fireworks over time at random x positions.
    """
    def __init__(self, ground_y, spawn_interval=2.0):
        super().__init__()
        self.ground_y = ground_y
        self.spawn_interval = spawn_interval
        self._time_since_last = 0.0
        self.children = []  # store individual FireworkEffect objects

    def reset(self):
        super().reset()
        self._time_since_last = 0.0
        self.children.clear()

    def update(self, dt):
        super().update(dt)
        if not self.is_active:
            return
        self._time_since_last += dt
        if self._time_since_last >= self.spawn_interval:
            self._time_since_last = 0.0
            # spawn a new firework
            x = random.randint(50, pygame.display.get_surface().get_width()-50)
            color = (
                random.randint(128,255),
                random.randint(128,255),
                random.randint(128,255)
            )
            fw = FireworkEffect(x, self.ground_y, color)
            self.children.append(fw)

        # update children
        for c in self.children:
            c.update(dt)
        # remove killed
        self.children = [c for c in self.children if not c._should_remove]

    def draw(self, screen):
        if not self.is_active:
            return
        for c in self.children:
            c.draw(screen)


def main():
    pygame.init()
    engine = Engine(width=800, height=600, title="CybrHUD Fireworks Demo")

    # The ground will be near the bottom
    ground_y = 550

    # Starry background
    background = StarryBackground(
        image_path="assets/images/starry_sky.png", # optional
        star_count=150
    )

    # Spawner of fireworks
    fw_manager = FireworksManager(ground_y=ground_y, spawn_interval=1.5)

    # Build a scene. Let it run for 15 seconds, or user can close early.
    scene = Scene(effects=[background, fw_manager], duration=15.0)

    engine.add_scene(scene)
    engine.run()

if __name__ == "__main__":
    main()
