#!/usr/bin/env python3
"""
demo_console.py

Shows an interactive "console" or "terminal" effect with typed user input.
 - The user can type lines, press Enter to add them to the log.
 - A "scanline" overlay is drawn to give it a retro-futuristic HUD feel.

Requires:
 - assets/fonts/Orbitron-Regular.ttf (or your own TTF)
 - assets/images/scanlines.png (optional overlay)
"""

import pygame
import sys
import time

from core.engine import Engine
from core.scene import Scene
from core.effect import Effect

# An Effect that provides a console input + scrolling log.

class ConsoleEffect(Effect):
    """
    A simple console effect:
     - A text input bar at the bottom
     - A scrollable log of lines at the top
     - User can press Enter to commit typed text to the log
    """
    def __init__(self, x, y, width, height, font_path=None, font_size=20, text_color=(0,255,0), bg_color=(10,10,10)):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.font_path = font_path
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color

        self._font = None
        self._lines = []
        self._input_buffer = ""
        self._cursor_visible = True
        self._cursor_timer = 0.0
        self._cursor_interval = 0.5  # blink rate

        # for scrolling
        self.scroll_offset = 0

    def reset(self):
        super().reset()
        if self.font_path:
            self._font = pygame.font.Font(self.font_path, self.font_size)
        else:
            self._font = pygame.font.SysFont("Courier", self.font_size)

        self._lines.clear()
        self._input_buffer = ""
        self.scroll_offset = 0
        self._cursor_visible = True
        self._cursor_timer = 0.0

    def handle_event(self, event):
        if not self.is_active:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # commit typed text
                text_to_add = self._input_buffer.strip()
                if text_to_add:
                    self._lines.append(text_to_add)
                self._input_buffer = ""
                # auto-scroll to bottom
                self.scroll_offset = 0

            elif event.key == pygame.K_BACKSPACE:
                self._input_buffer = self._input_buffer[:-1]
            elif event.key == pygame.K_UP:
                # scroll up
                self.scroll_offset += 1
            elif event.key == pygame.K_DOWN:
                # scroll down
                self.scroll_offset = max(0, self.scroll_offset - 1)
            else:
                # add typed character
                ch = event.unicode
                if ch.isprintable():
                    self._input_buffer += ch

    def update(self, dt):
        super().update(dt)
        if not self.is_active:
            return
        # blink cursor
        self._cursor_timer += dt
        if self._cursor_timer >= self._cursor_interval:
            self._cursor_timer = 0.0
            self._cursor_visible = not self._cursor_visible

    def draw(self, screen):
        if not self.is_active:
            return

        # draw background
        console_surf = pygame.Surface((self.rect.width, self.rect.height))
        console_surf.fill(self.bg_color)

        # draw log lines
        line_height = self._font.get_height()
        visible_lines = self.rect.height // line_height - 2  # minus 2 lines for the input bar
        # start from the bottom
        start_idx = max(0, len(self._lines) - visible_lines - self.scroll_offset)
        end_idx = len(self._lines) - self.scroll_offset

        y_off = 0
        for line in self._lines[start_idx:end_idx]:
            txt_surf = self._font.render(line, True, self.text_color)
            console_surf.blit(txt_surf, (5, y_off))
            y_off += line_height

        # draw input line
        input_text = self._input_buffer
        if self._cursor_visible:
            input_text += "_"
        input_surf = self._font.render("> " + input_text, True, self.text_color)
        console_surf.blit(input_surf, (5, self.rect.height - line_height - 5))

        screen.blit(console_surf, (self.rect.x, self.rect.y))


class ScanlineOverlay(Effect):
    """
    A subtle scanning line overlay for a retro or futuristic look.
    Repeats an image texture (e.g. horizontal lines) across the screen with some alpha.
    """
    def __init__(self, image_path, alpha=80):
        super().__init__()
        self.image_path = image_path
        self.alpha = alpha
        self._texture = None

    def reset(self):
        super().reset()
        if self.image_path:
            self._texture = pygame.image.load(self.image_path).convert()
            self._texture.set_alpha(self.alpha)

    def draw(self, screen):
        if not self.is_active or not self._texture:
            return
        tex_w = self._texture.get_width()
        tex_h = self._texture.get_height()
        sw, sh = screen.get_size()

        # tile the texture across the screen
        for y in range(0, sh, tex_h):
            for x in range(0, sw, tex_w):
                screen.blit(self._texture, (x, y))


def main():
    pygame.init()
    engine = Engine(width=1000, height=600, title="Futuristic Console Demo")

    # Build the console effect
    # Provide a fancy font if available in assets
    console = ConsoleEffect(
        x=50, y=50, width=900, height=400,
        font_path="assets/fonts/Orbitron-Regular.ttf", font_size=22,
        text_color=(0,255,0), bg_color=(30,30,30)
    )
    overlay = ScanlineOverlay(image_path="assets/images/scanlines.png", alpha=40)

    scene = Scene(
        effects=[console, overlay],
        duration=0  # run indefinitely or until user quits
    )

    engine.add_scene(scene)
    engine.run()

if __name__ == "__main__":
    main()
