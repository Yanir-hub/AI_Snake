import pygame
from constants import *

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.difficulty_options = ['easy', 'medium', 'hard']
        self.current_difficulty = 1  # Default to medium
        self.speed_options = ['Slow', 'Normal', 'Fast']
        self.current_speed = 1  # Default to normal

    def draw(self, screen, selected_option=0):
        screen.fill(BLACK)

        title = self.font.render("Snake Game", True, WHITE)
        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))

        options = ["Single Player", "VS AI", "Quit"]
        for i, option in enumerate(options):
            color = GREEN if i == selected_option else WHITE
            text = self.font.render(option, True, color)
            screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, 250 + i * 60))

    def draw_difficulty_selector(self, screen):
        screen.fill(BLACK)

        title = self.font.render("Select AI Difficulty", True, WHITE)
        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))

        for i, diff in enumerate(self.difficulty_options):
            color = GREEN if i == self.current_difficulty else WHITE
            text = self.font.render(diff.capitalize(), True, color)
            screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, 250 + i * 60))

        instructions = self.small_font.render("Use UP/DOWN to change, ENTER to confirm", True, WHITE)
        screen.blit(instructions, (WINDOW_WIDTH//2 - instructions.get_width()//2, 450))

    def draw_speed_selector(self, screen):
        screen.fill(BLACK)

        title = self.font.render("Select Snake Speed", True, WHITE)
        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))

        for i, speed in enumerate(self.speed_options):
            color = GREEN if i == self.current_speed else WHITE
            text = self.font.render(speed, True, color)
            screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, 250 + i * 60))

        instructions = self.small_font.render("Use UP/DOWN to change, ENTER to confirm", True, WHITE)
        screen.blit(instructions, (WINDOW_WIDTH//2 - instructions.get_width()//2, 450))

    def draw_win_condition_selector(self, screen, apples):
        screen.fill(BLACK)

        title = self.font.render("Select Apple Target", True, WHITE)
        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))

        value = self.font.render(str(apples), True, GREEN)
        screen.blit(value, (WINDOW_WIDTH//2 - value.get_width()//2, 250))

        instructions = self.small_font.render("Use UP/DOWN to change, ENTER to start", True, WHITE)
        screen.blit(instructions, (WINDOW_WIDTH//2 - instructions.get_width()//2, 350))
