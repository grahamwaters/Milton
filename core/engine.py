"""
core/engine.py

Manages:
 - a list of Scenes
 - main loop
 - optional transitions between Scenes
 - set_scene(index) to jump around
"""

import pygame
import sys
import time

from core.scene import Scene
from core.transition import FadeTransition, GlitchTransition

class Engine:
    def __init__(self, width=800, height=600, title="CybrHUD Demo", fps=60):
        """
        :param fps: target frames per second
        """
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.fps = fps

        self.scenes = []
        self.active_scene_index = 0
        self.running = False

        # optional transitions
        self.transition_in = None  # e.g. FadeTransition(...) for each scene
        self.transition_out = None

    def add_scene(self, scene: Scene):
        self.scenes.append(scene)

    def set_scene(self, index):
        """
        Jump to a specific scene index, if valid.
        """
        if 0 <= index < len(self.scenes):
            self.active_scene_index = index

    def run(self):
        self.running = True

        while self.running and self.active_scene_index < len(self.scenes):
            scene = self.scenes[self.active_scene_index]
            scene.reset(self)

            # Optional transition in
            if self.transition_in:
                self._play_transition(self.transition_in)

            # run scene
            start_time = time.time()
            while scene.playing and self.running:
                dt = self.clock.tick(self.fps)/1000.0

                # handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.running = False
                    scene.handle_event(event)

                scene.update(dt)
                scene.draw(self.screen)
                pygame.display.flip()

            # Optional transition out
            if self.running and self.transition_out:
                self._play_transition(self.transition_out)

            # next scene
            self.active_scene_index += 1

        pygame.quit()
        sys.exit()

    def _play_transition(self, transition_factory):
        """
        Plays a transition for e.g. 1 second. The transition_factory
        is a function that returns an Effect or a list of Effects
        used for the transitional scene.
        """
        # we create a temporary "transition scene"
        transition_effect = transition_factory()
        if not isinstance(transition_effect, list):
            transition_effect = [transition_effect]
        temp_scene = Scene(effects=transition_effect, duration=0)
        temp_scene.reset(self)

        # run until all are done or user quits
        # we'll define a short max time
        max_time = 2.0
        start_t = time.time()

        while True:
            dt = self.clock.tick(self.fps)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

            if not self.running:
                break

            temp_scene.update(dt)

            # if all transitions are done or we exceed max_time
            if all(e._should_remove for e in temp_scene.effects) or (time.time()-start_t>=max_time):
                break

            temp_scene.draw(self.screen)
            pygame.display.flip()
