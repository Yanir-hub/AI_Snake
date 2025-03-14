import pygame
from constants import *

class Snake:
    def __init__(self, x, y, color):
        self.body = [(x, y)]
        self.direction = RIGHT
        self.color = color
        self.growing = False
        self.score = 0

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

    def change_direction(self, new_direction):
        # Prevent 180-degree turns
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def grow(self):
        self.growing = True
        self.score += 1

    def check_collision(self, other_snake=None):
        head = self.body[0]
        
        # Wall collision
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True

        # Self collision
        if head in self.body[1:]:
            return True

        # Other snake collision
        if other_snake:
            if head in other_snake.body:
                return True

        return False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, self.color,
                           (segment[0] * GRID_SIZE,
                            segment[1] * GRID_SIZE,
                            GRID_SIZE - 2,
                            GRID_SIZE - 2))
