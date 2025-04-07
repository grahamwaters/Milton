#!/usr/bin/env python3
"""
demo_glitch_transition.py

Shows how to use a glitch transition effect between two Scenes.
We'll create 2 simple Scenes with some text or shapes,
then apply a glitch effect in between.
"""

import sys
import pygame

from core.engine import Engine
from core.scene import Scene
from core.hud.text import TextBlock
from core.hud.shapes import HexGrid
from core.transition import GlitchTransition

def main():
    engine = Engine(width=1280, height=720, title="Glitch Transition Demo")

    # First scene
    scene1_effects = [
        HexGrid(color=(80,0,80), cell_size=60),
        TextBlock("SCENE 1 - Press any key to go to SCENE 2", 100, 100, font_size=32, color=(255,255,255)),
    ]
    scene1 = Scene(effects=scene1_effects, duration=0)  # indefinite until user triggers

    # Second scene
    scene2_effects = [
        TextBlock("SCENE 2 - The glitch transition is complete!", 100, 200, font_size=32, color=(0,255,0)),
    ]
    scene2 = Scene(effects=scene2_effects, duration=3.0)  # after 3s, ends

    # We'll insert a short "transition scene" with the glitch effect
    glitch_scene = Scene(effects=[GlitchTransition(duration=2.0)], duration=2.0)

    engine.add_scene(scene1)
    engine.add_scene(glitch_scene)
    engine.add_scene(scene2)

    engine.run()

if __name__ == "__main__":
    main()
