"""
core/scene.py

Scene class: container for multiple Effects.
New features:
 - z-order sorting each frame
 - add_effect(), remove_effect(), find_effects()
 - indefinite or timed Scenes
"""

import pygame

class Scene:
    def __init__(self, effects=None, duration=0.0):
        """
        :param effects: list of Effects
        :param duration: scene ends after this many seconds if > 0
        """
        self.effects = effects if effects else []
        self.duration = duration
        self.playing = True
        self.engine = None

        self._time_in_scene = 0.0

    def reset(self, engine):
        """
        Called by the Engine when the Scene starts.
        """
        self.engine = engine
        self.playing = True
        self._time_in_scene = 0.0

        for e in self.effects:
            e.reset()

    def add_effect(self, effect):
        """
        Dynamically add an Effect to the scene.
        """
        effect.reset()
        self.effects.append(effect)

    def remove_effect(self, effect):
        """
        Dynamically remove an Effect from the scene.
        """
        if effect in self.effects:
            self.effects.remove(effect)

    def find_effects(self, effect_type):
        """
        Returns a list of effects of the given class/type.
        """
        return [e for e in self.effects if isinstance(e, effect_type)]

    def handle_event(self, event):
        """
        Pass events to all Effects if they're active.
        """
        for e in self.effects:
            if e.is_active:
                e.handle_event(event)

        # Example: handle window resize
        if event.type == pygame.VIDEORESIZE:
            # For demonstration, let's just center the scene or do something
            # Actually you'd recalc positions. We'll skip for brevity.
            pass

    def update(self, dt):
        """
        Update all Effects. Sort them by z_order. Remove dead ones.
        """
        self._time_in_scene += dt
        for e in self.effects:
            e.update(dt)

        # remove dead
        self.effects = [e for e in self.effects if not e._should_remove]

        # sort by z_order ascending
        self.effects.sort(key=lambda e: e.z_order)

        # if scene has a finite duration
        if self.duration > 0 and self._time_in_scene >= self.duration:
            self.playing = False

    def draw(self, screen):
        """
        Clear screen (or draw a background), then draw Effects in z_order.
        """
        screen.fill((0,0,0))

        for e in self.effects:
            if e.is_active:
                e.draw(screen)
