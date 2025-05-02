import pygame
import random
from game.constants import *

class PowerUp:
    def __init__(self):
        self.position = None
        self.spawn()

    def spawn(self):
        while True:
            pos = (random.randint(2, GRID_WIDTH-3), 
                  random.randint(2, GRID_HEIGHT-3))
            # Will be checked against snake positions in game loop
            self.position = pos
            return

    def draw(self, screen):
        if not self.position:
            return

        x, y = self.position
        center = (x * GRID_SIZE + GRID_SIZE//2, y * GRID_SIZE + GRID_SIZE//2)
        radius = GRID_SIZE//2 - 2

        # Draw freeze power-up (blue circle with 'F')
        color = (0, 191, 255)  # Deep Sky Blue
        pygame.draw.circle(screen, color, center, radius)

        # Draw text
        font = pygame.font.Font(None, 20)
        text_surface = font.render('F', True, WHITE)
        text_rect = text_surface.get_rect(center=center)
        screen.blit(text_surface, text_rect)

class PowerUpEffect:
    def __init__(self, duration=300):  # 300 frames = 5 seconds at 60 FPS
        self.duration = duration
        self.remaining = duration

    def update(self):
        if self.remaining > 0:
            self.remaining -= 1
        return self.remaining > 0