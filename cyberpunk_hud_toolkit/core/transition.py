"""
core/transition.py

Example transition effects: fade, glitch, etc.
Transitions can be invoked when switching Scenes or layered on top of Scenes.
"""
import pygame
import random
from core.effect import Effect

class FadeTransition(Effect):
    """
    Simple fade-in or fade-out transition effect.
    """
    def __init__(self, duration=1.0, fade_in=True):
        super().__init__()
        self.duration = duration
        self.fade_in = fade_in
        self.elapsed = 0.0
        self.alpha = 255 if fade_in else 0

    def reset(self):
        self.elapsed = 0.0
        self.alpha = 255 if self.fade_in else 0

    def update(self, dt):
        self.elapsed += dt
        progress = min(1.0, self.elapsed / self.duration)
        if self.fade_in:
            # alpha goes from 255 -> 0
            self.alpha = int(255 - 255 * progress)
        else:
            # alpha goes from 0 -> 255
            self.alpha = int(255 * progress)

    def draw(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0,0,0,self.alpha))  # black fill with alpha
        screen.blit(overlay, (0,0))


class GlitchTransition(Effect):
    """
    Quick hacky glitch transition:
     - randomly shifts horizontal slices of the screen
     - overlay with semi-transparent noise
    """
    def __init__(self, duration=1.0):
        super().__init__()
        self.duration = duration
        self.elapsed = 0.0

        # We won't store the screen content inside the effect, so we rely
        # on the scene to call this effect's draw last.
        # Alternatively, you'd capture a screenshot once the transition starts.

    def reset(self):
        self.elapsed = 0.0

    def update(self, dt):
        self.elapsed += dt

    def draw(self, screen):
        progress = min(1.0, self.elapsed / self.duration)
        # We'll do a few random slices
        overlay = pygame.Surface(screen.get_size())
        overlay.blit(screen, (0,0))
        for _ in range(5):
            slice_y = random.randint(0, screen.get_height()-10)
            slice_h = random.randint(5, 20)
            offset_x = random.randint(-20, 20)
            region = overlay.subsurface((0, slice_y, screen.get_width(), slice_h))
            screen.blit(region, (offset_x, slice_y))

        # Draw some noise
        noise_surf = pygame.Surface(screen.get_size())
        noise_surf.fill((0,0,0))
        for _ in range(200):
            nx = random.randint(0, screen.get_width()-1)
            ny = random.randint(0, screen.get_height()-1)
            noise_surf.set_at((nx, ny), (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        noise_surf.set_alpha(int(80*(1.0-progress)))
        screen.blit(noise_surf, (0,0))
