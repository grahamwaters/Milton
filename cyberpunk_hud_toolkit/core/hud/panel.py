"""
core/hud/panel.py

Glowing or translucent panels that can slide in/out.
"""
import pygame
from core.effect import Effect

class SlidingPanel(Effect):
    def __init__(self, x, y, width, height, color=(20,20,20), glow_color=(0,200,200), direction='up', speed=200):
        """
        :param direction: up/down/left/right from which the panel slides in
        """
        super().__init__()
        self.x = x
        self.y = y
        self.final_x = x
        self.final_y = y
        self.width = width
        self.height = height
        self.color = color
        self.glow_color = glow_color
        self.direction = direction
        self.speed = speed
        self._visible = False

        # Start position off-screen
        if direction == 'up':
            self.y = pygame.display.get_surface().get_height()
        elif direction == 'down':
            self.y = -height
        elif direction == 'left':
            self.x = -width
        elif direction == 'right':
            self.x = pygame.display.get_surface().get_width()

    def update(self, dt):
        if not self._visible:
            # Slide into final position
            dx = self.final_x - self.x
            dy = self.final_y - self.y
            dist = (dx**2 + dy**2)**0.5
            if dist > 5:
                angle = pygame.math.atan2(dy, dx)
                self.x += self.speed * dt * pygame.math.cos(angle)
                self.y += self.speed * dt * pygame.math.sin(angle)
            else:
                self.x, self.y = self.final_x, self.final_y
                self._visible = True

    def draw(self, screen):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Draw background
        panel_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        panel_surf.fill((*self.color, 180))  # semi-translucent

        # Glow border
        pygame.draw.rect(panel_surf, self.glow_color, (0,0,self.width,self.height), 2)

        screen.blit(panel_surf, rect)
