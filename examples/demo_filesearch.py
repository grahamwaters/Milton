#!/usr/bin/env python3
"""
demo_filesearch.py

Simulates a futuristic file-search with scanning bars, highlighting,
and relevant/irrelevant classification.

Pages:
 - Rise from bottom
 - Get scanned by a black bar
 - Words relevant to the search highlight in green
 - If relevant, page slides to a stack on the right
 - If not, page fades to gray and drifts away

Auto-ends after 5 minutes or if user presses ESC.
"""
import pygame
import sys
import time
import random

from core.engine import Engine
from core.scene import Scene
from core.effect import Effect

SEARCH_DURATION = 300.0  # 5 minutes

SYNONYMS_MAP = {
    "apple": ["macintosh", "ios", "ipad", "iphone", "orchard"],
    "tree":  ["forest", "wood", "branch", "roots", "canopy"],
    "secret":["classified", "hidden", "undercover", "covert"],
}

DEMO_FILES = [
    "apple_pie_recipe.txt",
    "secret_plans.doc",
    "maple_tree_diagram.png",
    "holiday_photos_2022.zip",
    "random_notes.txt",
    "classified_research.pdf",
    "tree_of_life_theory.docx",
    "iphone_review_article.md",
    "misc_apple_picking.jpg",
    "unknown_document.doc"
]


class FilePage(Effect):
    def __init__(self, filename, synonyms):
        super().__init__()
        self.filename = filename
        self.synonyms = synonyms
        self.words_in_file = self._mock_file_contents()

        self.is_relevant = any(w.lower() in synonyms for w in self.words_in_file)
        self.x = 200
        self.y = 800
        self.width = 300
        self.height = 150

        self.scan_progress = 0.0
        self.state = "rising"  # rising -> scanning -> done
        self.timer = 0.0
        self.alpha = 255
        self.scale = 1.0
        self.drift_dir = random.choice([-1,1])
        self._font = None

    def reset(self):
        # Called each time scene starts
        # Not strictly needed, but could reset position if desired
        pass

    def _mock_file_contents(self):
        # Just split filename + some random words
        name_tokens = self.filename.replace(".", " ").replace("_", " ").split()
        extra_words = ["apple", "tree", "secret", "random", "stuff", "notes"]
        random.shuffle(extra_words)
        return name_tokens + extra_words[:3]

    def update(self, dt):
        if self.state == "rising":
            self.y -= 100 * dt
            if self.y <= 200:
                self.y = 200
                self.state = "scanning"
                self.timer = 0.0
                self.scan_progress = 0.0
        elif self.state == "scanning":
            self.timer += dt
            scan_time = 2.0
            self.scan_progress = min(1.0, self.timer / scan_time)
            if self.scan_progress >= 1.0:
                self.state = "done"
        else:
            # done
            if self.is_relevant:
                # slide to the right stack
                self.x += 200 * dt
                if self.x >= 700:
                    self.x = 700
            else:
                # fade out and drift away
                self.alpha = max(0, self.alpha - 80*dt)
                self.scale = max(0.1, self.scale - 0.2*dt)
                self.y -= 20 * dt
                self.x += self.drift_dir * 40 * dt

    def draw(self, screen):
        if self._font is None:
            self._font = pygame.font.SysFont("Arial", 18)

        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # color page
        if self.is_relevant:
            page_color = (240, 240, 240)
        else:
            g = int(240 * (self.alpha / 255))
            page_color = (g, g, g)
        surf.fill(page_color)

        # Render text
        text_lines = [f"FILE: {self.filename}", "Content: " + " ".join(self.words_in_file[:5]) + "..."]
        y_off = 10
        for line in text_lines:
            r_line = self._render_highlight(line)
            surf.blit(r_line, (10, y_off))
            y_off += 25

        if self.state == "scanning":
            bar_width = int(self.width * self.scan_progress)
            pygame.draw.rect(surf, (0,0,0), (0,0,bar_width,self.height))

        if self.scale < 1.0:
            w_scaled = int(self.width * self.scale)
            h_scaled = int(self.height * self.scale)
            surf = pygame.transform.smoothscale(surf, (w_scaled, h_scaled))

        if self.alpha < 255:
            surf.set_alpha(int(self.alpha))

        rect = surf.get_rect(center=(self.x, self.y))
        screen.blit(surf, rect)

    def _render_highlight(self, text):
        # highlight synonyms in green
        container = pygame.Surface((self.width, 25), pygame.SRCALPHA)
        words = text.split()
        x_off = 0
        for w in words:
            color = (0,0,0)
            if w.lower() in self.synonyms:
                color = (0,180,0)
            label = self._font.render(w+" ", True, color)
            container.blit(label, (x_off, 0))
            x_off += label.get_width()
        return container


class FileSearchScene(Scene):
    def __init__(self, search_term, synonyms_set, duration=SEARCH_DURATION):
        super().__init__(duration=duration)
        # Shuffle files
        shuffled_files = DEMO_FILES[:]
        random.shuffle(shuffled_files)
        # Create pages
        self.effects = [
            FilePage(f, synonyms_set) for f in shuffled_files
        ]

def main():
    pygame.init()
    screen_w, screen_h = 1280, 720

    # Pick random search term from synonyms
    search_term = random.choice(list(SYNONYMS_MAP.keys()))
    synonyms_set = set([search_term] + SYNONYMS_MAP[search_term])

    engine = Engine(width=screen_w, height=screen_h, title="Futuristic File Search")
    scene = FileSearchScene(search_term, synonyms_set, duration=SEARCH_DURATION)
    engine.add_scene(scene)
    engine.run()

if __name__ == "__main__":
    main()
