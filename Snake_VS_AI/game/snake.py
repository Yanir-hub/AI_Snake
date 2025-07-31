import pygame
from game.constants import *

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
        # Draw body
        for segment in self.body:
            pygame.draw.rect(screen, self.color,
                           (segment[0] * GRID_SIZE,
                            segment[1] * GRID_SIZE,
                            GRID_SIZE - 2,
                            GRID_SIZE - 2))

        # Draw face on head
        head = self.body[0]
        head_x = head[0] * GRID_SIZE
        head_y = head[1] * GRID_SIZE

        # Draw eyes
        eye_color = (0, 0, 0)  # Black eyes
        eye_radius = GRID_SIZE // 6

        # Adjust eye positions based on direction
        if self.direction == RIGHT:
            eye_pos = [(head_x + 3*GRID_SIZE//4, head_y + GRID_SIZE//3),
                      (head_x + 3*GRID_SIZE//4, head_y + 2*GRID_SIZE//3)]
        elif self.direction == LEFT:
            eye_pos = [(head_x + GRID_SIZE//4, head_y + GRID_SIZE//3),
                      (head_x + GRID_SIZE//4, head_y + 2*GRID_SIZE//3)]
        elif self.direction == UP:
            eye_pos = [(head_x + GRID_SIZE//3, head_y + GRID_SIZE//4),
                      (head_x + 2*GRID_SIZE//3, head_y + GRID_SIZE//4)]
        else:  # DOWN
            eye_pos = [(head_x + GRID_SIZE//3, head_y + 3*GRID_SIZE//4),
                      (head_x + 2*GRID_SIZE//3, head_y + 3*GRID_SIZE//4)]

        for pos in eye_pos:
            pygame.draw.circle(screen, eye_color, pos, eye_radius)