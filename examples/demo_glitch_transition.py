#!/usr/bin/env python3
"""
demo_glitch_transition.py

Now uses the new SlideTransition as well for the outbound.
"""

import pygame
from core.engine import Engine
from core.scene import Scene
from core.hud.text import TextBlock
from core.hud.shapes import HexGrid
from core.transition import GlitchTransition, SlideTransition

def main():
    engine = Engine(width=1280, height=720, title="Glitch + Slide Transition Demo")

    # We'll define a function that returns a glitch effect for engine.transition_in,
    # and a function that returns a slide for engine.transition_out.
    engine.transition_in = lambda: GlitchTransition(duration=1.5)
    engine.transition_out = lambda: SlideTransition(duration=1.2, direction='left')

    scene1 = Scene(effects=[
        HexGrid(color=(80,0,80), cell_size=60),
        TextBlock("SCENE 1 - Press ESC to exit, or wait ~5s to end", 100, 100, font_size=32, color=(255,255,255)),
    ], duration=5.0)

    scene2 = Scene(effects=[
        TextBlock("SCENE 2 - The glitch->slide transitions are done!", 100, 200, font_size=32, color=(0,255,0)),
    ], duration=5.0)

    engine.add_scene(scene1)
    engine.add_scene(scene2)

    engine.run()

if __name__ == "__main__":
    main()
