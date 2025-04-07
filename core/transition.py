"""
core/transition.py

More robust transitions:
 - FadeTransition (in or out)
 - GlitchTransition with random horizontal slices
 - SlideTransition (optional)
"""

import pygame
import random
import time
import math
from core.effect import Effect

class FadeTransition(Effect):
    """
    Fade in or out over `duration` seconds
    If fade_in=True, alpha goes 255->0
    If fade_in=False, alpha goes 0->255
    """
    def __init__(self, duration=1.0, fade_in=True, color=(0,0,0)):
        super().__init__(z_order=9999)
        self.duration = duration
        self.fade_in = fade_in
        self.color = color
        self.elapsed = 0.0
        self.alpha = 255 if fade_in else 0

    def reset(self):
        super().reset()
        self.elapsed = 0.0
        self.alpha = 255 if self.fade_in else 0

    def update(self, dt):
        super().update(dt)
        if not self.is_active:
            return
        self.elapsed += dt
        progress = min(1.0, self.elapsed / self.duration)
        if self.fade_in:
            self.alpha = int(255 - 255 * progress)
        else:
            self.alpha = int(255 * progress)

        if progress >= 1.0:
            # done
            self.kill()

    def draw(self, screen):
        if not self.is_active:
            return
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        # color fill with alpha
        overlay.fill((*self.color, self.alpha))
        screen.blit(overlay, (0,0))


class GlitchTransition(Effect):
    """
    Glitch: random horizontal slices offset, plus noise overlay.
    """
    def __init__(self, duration=1.0):
        super().__init__(z_order=9999)
        self.duration = duration
        self.start_surf = None
        self.elapsed = 0.0

    def reset(self):
        super().reset()
        self.start_surf = None
        self.elapsed = 0.0

    def update(self, dt):
        super().update(dt)
        if not self.is_active:
            return
        self.elapsed += dt
        if self.duration > 0 and self.elapsed >= self.duration:
            self.kill()

    def draw(self, screen):
        if not self.is_active:
            return
        if self.start_surf is None:
            # capture screen
            self.start_surf = screen.copy()

        # start by blitting the captured screen
        screen.blit(self.start_surf, (0,0))

        # slice offset
        h = screen.get_height()
        w = screen.get_width()
        for _ in range(5):
            slice_y = random.randint(0, h-10)
            slice_h = random.randint(5, 20)
            offset_x = random.randint(-20, 20)
            region = self.start_surf.subsurface((0, slice_y, w, slice_h))
            screen.blit(region, (offset_x, slice_y))

        # draw noise
        noise_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        for _ in range(300):
            nx = random.randint(0, w-1)
            ny = random.randint(0, h-1)
            noise_surf.set_at((nx, ny), (random.randint(0,255), random.randint(0,255), random.randint(0,255), 80))
        screen.blit(noise_surf, (0,0))


class SlideTransition(Effect):
    """
    A slide transition that shifts the old screen left or right as it reveals the new.
    For demonstration, we'll just shift the old screen out of view horizontally.

    If direction='left', it slides left. 'right' slides right.
    """
    def __init__(self, duration=1.0, direction='left'):
        super().__init__(z_order=9999)
        self.duration = duration
        self.direction = direction
        self.start_surf = None
        self.elapsed = 0.0

    def reset(self):
        super().reset()
        self.start_surf = None
        self.elapsed = 0.0

    def update(self, dt):
        super().update(dt)
        if not self.is_active:
            return
        self.elapsed += dt
        if self.duration > 0 and self.elapsed >= self.duration:
            self.kill()

    def draw(self, screen):
        if not self.is_active:
            return
        if self.start_surf is None:
            self.start_surf = screen.copy()

        w = screen.get_width()
        progress = min(1.0, self.elapsed/self.duration)
        offset = int(progress * w)  # moves from 0 to w

        if self.direction == 'left':
            screen.blit(self.start_surf, (-offset, 0))
        else:
            screen.blit(self.start_surf, (offset, 0))
