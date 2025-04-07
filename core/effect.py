"""
core/effect.py

A robust Base Effect class for Scenes. Provides:
 - z_order for render sorting
 - optional start_delay & duration
 - is_active logic
 - kill() method to remove itself from the Scene
 - event handling stubs
 - bounding-box overlap helper
"""

import pygame
import time

class Effect:
    """
    Base effect that the Scene will manage and update.
    Extend this to create your own animations, widgets, transitions, etc.
    """

    def __init__(self, z_order=0, start_delay=0.0, duration=0.0):
        """
        :param z_order: higher means drawn on top
        :param start_delay: time in seconds to wait before effect becomes active
        :param duration: if > 0, effect auto-removes after this many seconds
        """
        self.z_order = z_order
        self.start_delay = start_delay
        self.duration = duration

        self._start_time = None
        self._is_active = False
        self._should_remove = False

    def reset(self):
        """
        Called by the Scene at the start of each run or re-run.
        """
        self._start_time = None
        self._is_active = False
        self._should_remove = False

    def handle_event(self, event):
        """
        Override to respond to keyboard/mouse events, etc.
        """
        pass

    def update(self, dt):
        """
        Called each frame with the time delta in seconds.
        """
        # Mark start_time if not already
        if self._start_time is None:
            self._start_time = time.time()

        elapsed = time.time() - self._start_time
        # Check if we are past the start_delay
        if not self._is_active and elapsed >= self.start_delay:
            self._is_active = True

        # If there's a duration and we've exceeded it, kill ourselves
        if self.duration > 0 and elapsed >= (self.start_delay + self.duration):
            self.kill()

    def draw(self, screen):
        """
        Override to draw your effect. Only draw if is_active is True.
        """
        pass

    def kill(self):
        """
        Mark this effect for removal.
        """
        self._should_remove = True

    @property
    def is_active(self):
        """
        True if the effect is currently active (time >= start_delay) and not removed.
        """
        return self._is_active and not self._should_remove

    def overlaps(self, other, rect_self, rect_other):
        """
        Bounding box collision helper.
        :return: True if rect_self collides with rect_other
        """
        return rect_self.colliderect(rect_other)
