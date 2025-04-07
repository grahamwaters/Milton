"""
core/scene.py

Scene class that holds multiple Effects and orchestrates them.
"""
import pygame

class Scene:
    def __init__(self, effects=None, duration=0.0):
        """
        :param effects: List of Effects in this scene
        :param duration: If > 0, the scene ends after `duration` seconds
        """
        self.effects = effects if effects else []
        self.duration = duration
        self.playing = True
        self.engine = None  # Will be set when scene is started

    def reset(self, engine):
        """
        Reset scene state. Called by Engine when first starting the scene.
        """
        self.engine = engine
        self.playing = True
        # Reset each effect if needed
        for eff in self.effects:
            eff.reset()

    def handle_event(self, event):
        """
        Pass input events to each effect if they need it.
        """
        for eff in self.effects:
            eff.handle_event(event)

    def update(self, dt):
        """
        Update logic for all effects in the scene.
        """
        for eff in self.effects:
            eff.update(dt)

    def draw(self, screen):
        """
        Clear the screen or draw a background, then draw all effects.
        """
        screen.fill((0,0,0))  # black background (or any)
        for eff in self.effects:
            eff.draw(screen)
