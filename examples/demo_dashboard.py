#!/usr/bin/env python3
"""
demo_dashboard.py

Shows a futuristic "dashboard" scene with:
 - background hex grid
 - sliding panel
 - circular progress meters
 - a radar sweep
 - text blocks
"""
import sys
import pygame

# from core.engine import Engine
# from core.engine import Engine
from MILTON.core.engine import Engine

from core.scene import Scene
from core.hud.circular import CircularProgress
from core.hud.panel import SlidingPanel
from core.hud.radar import RadarSweep
from core.hud.shapes import HexGrid
from core.hud.text import TextBlock
from core.hud.particles import ParticleEmitter
# In cyberpunk_hud_toolkit/examples/demo_dashboard.py

# from cyberpunk_hud_toolkit.core.engine import Engine

def main():
    engine = Engine(width=1280, height=720, title="CybrHUD Dashboard Demo")

    # Effects
    background_grid = HexGrid(color=(40,40,70), cell_size=50)
    panel = SlidingPanel(100, 100, 400, 300, direction='left')
    radar = RadarSweep(x=900, y=300, radius=150)
    meter = CircularProgress(x=300, y=250, radius=80, value=0.25, color=(0,200,200))
    meter.speed = 0.1  # animate up slowly
    text1 = TextBlock("SYSTEM STATUS", 130, 110, font_size=28, color=(255,255,255))
    emitter = ParticleEmitter(x=640, y=360, color=(0,255,255))

    # Put them in a scene
    scene = Scene(effects=[background_grid, emitter, panel, radar, meter, text1], duration=10.0)
    engine.add_scene(scene)

    engine.run()

if __name__ == "__main__":
    main()
