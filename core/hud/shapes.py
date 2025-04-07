"""
core/hud/shapes.py

Drawing futuristic vector shapes, grids, crosshairs, etc.
"""
import pygame
import math
from core.effect import Effect

class HexGrid(Effect):
    """
    Example effect: draws a hexagonal grid as a background or overlay.
    """
    def __init__(self, color=(100,100,100), cell_size=30):
        super().__init__()
        self.color = color
        self.cell_size = cell_size

    def draw(self, screen):
        width, height = screen.get_size()
        for y in range(0, height, self.cell_size):
            for x in range(0, width, int(self.cell_size*1.5)):
                # offset every other row
                offset = 0 if ((y//self.cell_size) % 2 == 0) else self.cell_size*0.75
                cx = x + offset
                cy = y
                points = []
                for angle_deg in range(0, 360, 60):
                    angle_rad = math.radians(angle_deg)
                    px = cx + math.cos(angle_rad)*self.cell_size*0.5
                    py = cy + math.sin(angle_rad)*self.cell_size*0.5
                    points.append((px, py))
                pygame.draw.polygon(screen, self.color, points, 1)
