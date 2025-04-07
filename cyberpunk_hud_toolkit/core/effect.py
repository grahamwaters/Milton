"""
core/effect.py

Base Effect class. Each effect is an updatable and drawable object.
"""
import pygame

class Effect:
    def __init__(self):
        pass

    def reset(self):
        """
        Called by the Scene when it's first started.
        Override if your effect needs to reset state.
        """
        pass

    def handle_event(self, event):
        """
        Handle input events if needed (keys, mouse, etc.)
        """
        pass

    def update(self, dt):
        """
        Called every frame with the time delta.
        """
        pass

    def draw(self, screen):
        """
        Draw the effect onto the screen surface.
        """
        pass
