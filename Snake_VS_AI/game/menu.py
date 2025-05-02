import pygame
from game.constants import *

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.difficulty_options = ['easy', 'medium', 'hard']
        self.current_difficulty = 1  # Default to medium
        self.speed_options = ['Slow', 'Normal', 'Fast']
        self.current_speed = 1  # Default to normal
        self.special_abilities_enabled = False

        # Color customization
        self.color_options = {
            'background': [(0, 0, 0), (50, 50, 50), (20, 20, 40)],  # Black, Dark Gray, Navy
            'player': [(0, 255, 0), (255, 255, 0), (0, 255, 255)],  # Green, Yellow, Cyan
            'ai': [(0, 0, 255), (255, 0, 255), (255, 128, 0)],      # Blue, Magenta, Orange
            'wall': [(139, 69, 19), (160, 82, 45), (101, 67, 33)]   # Different browns
        }
        self.current_colors = {
            'background': 0,
            'player': 0,
            'ai': 0,
            'wall': 0
        }

    def get_current_colors(self):
        return {
            'background': self.color_options['background'][self.current_colors['background']],
            'player': self.color_options['player'][self.current_colors['player']],
            'ai': self.color_options['ai'][self.current_colors['ai']],
            'wall': self.color_options['wall'][self.current_colors['wall']]
        }

    def draw(self, screen, selected_option=0):
        screen.fill(BLACK)

        title = self.font.render("Snake Game", True, WHITE)
        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))

        options = ["Single Player", "VS AI", "Customize Colors", "Quit"]
        for i, option in enumerate(options):
            color = GREEN if i == selected_option else WHITE
            text = self.font.render(option, True, color)
            screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, 250 + i * 60))

    def draw_color_selector(self, screen, current_item=0):
        screen.fill(BLACK)

        # Title at the top
        title = self.font.render("Color Customization", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
        screen.blit(title, title_rect)

        # Instructions between title and options
        instructions = self.small_font.render("Use LEFT/RIGHT to change color, UP/DOWN to select item", True, WHITE)
        instructions_rect = instructions.get_rect(center=(WINDOW_WIDTH//2, 170))
        screen.blit(instructions, instructions_rect)

        # Color options with proper spacing
        items = ["Background", "Player Snake", "AI Snake", "Walls", "Done"]
        start_y = 250  # Start items after instructions
        for i, item in enumerate(items):
            color = GREEN if i == current_item else WHITE
            text = self.font.render(item, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, start_y + i * 60))
            screen.blit(text, text_rect)

    def draw_special_abilities_selector(self, screen):
        screen.fill(BLACK)

        title = self.font.render("Enable Special Abilities?", True, WHITE)
        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))

        options = ["Yes", "No"]
        for i, option in enumerate(options):
            color = GREEN if (i == 0) == self.special_abilities_enabled else WHITE
            text = self.font.render(option, True, color)
            screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, 250 + i * 60))

        instructions = self.small_font.render("Use UP/DOWN to change, ENTER to confirm", True, WHITE)
        screen.blit(instructions, (WINDOW_WIDTH//2 - instructions.get_width()//2, 450))

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