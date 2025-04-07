#!/usr/bin/env python3
"""
demo_hud_elements.py

Showcases a variety of HUD elements in a simple rotating display:
 - CircularProgress
 - RadarSweep
 - SlidingPanel
 - Particles
 - etc.
"""
import pygame
from core.engine import Engine
from core.scene import Scene

from core.hud.circular import CircularProgress
from core.hud.radar import RadarSweep
from core.hud.panel import SlidingPanel
from core.hud.text import TextBlock
from core.hud.particles import ParticleEmitter

def main():
    engine = Engine(width=1280, height=720, title="HUD Elements Showcase")

    # Create various effects
    meter = CircularProgress(x=200, y=300, radius=80, value=0.3, color=(255, 100, 100))
    meter.speed = 0.2
    radar = RadarSweep(x=600, y=300, radius=100)
    panel = SlidingPanel(x=800, y=100, width=300, height=200, direction='right')
    text = TextBlock("HUD Elements Showcase", 100, 100, font_size=36, color=(0,255,255))
    emitter = ParticleEmitter(640, 360, color=(255,255,0))

    scene = Scene(effects=[meter, radar, panel, text, emitter], duration=10.0)
    engine.add_scene(scene)

    engine.run()

if __name__ == "__main__":
    main()
