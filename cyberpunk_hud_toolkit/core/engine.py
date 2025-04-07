"""
core/engine.py

Main Engine class for CybrHUD. Manages:
 - PyGame initialization
 - a list of Scenes
 - the main loop for updates & rendering
 - transitions between Scenes
"""
import pygame
import sys
import time

from core.scene import Scene


class Engine:
    def __init__(self, width=800, height=600, title="CybrHUD Demo", fps=60):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.fps = fps

        self.scenes = []
        self.active_scene_index = 0
        self.running = False
        self.start_time = 0

    def add_scene(self, scene: Scene):
        """
        Add a Scene to the queue. Scenes play in the order they are added,
        unless transitions or user input changes that.
        """
        self.scenes.append(scene)

    def run(self):
        """
        Main game loop. Cycles through Scenes, transitions, etc.
        """
        self.running = True
        self.start_time = time.time()

        while self.running and self.active_scene_index < len(self.scenes):
            scene = self.scenes[self.active_scene_index]
            scene.reset(self)  # reset scene if needed

            scene_start_time = time.time()
            while scene.playing and self.running:
                dt = self.clock.tick(self.fps) / 1000.0
                # Process events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                    scene.handle_event(event)

                scene.update(dt)
                scene.draw(self.screen)
                pygame.display.flip()

                # Check if scene duration is done
                if scene.duration > 0:
                    elapsed = time.time() - scene_start_time
                    if elapsed >= scene.duration:
                        scene.playing = False

            # Move to next scene
            self.active_scene_index += 1

        pygame.quit()
        sys.exit()
