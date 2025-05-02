import pygame
import random
from game.constants import *
from game.snake import Snake
from game.ai import SnakeAI
from game.menu import Menu
from game.powerup import PowerUp, PowerUpEffect

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.menu = Menu()
        self.frame_count = 0
        self.reset_game()

    def reset_game(self):
        colors = self.menu.get_current_colors()
        self.player = Snake(GRID_WIDTH // 4, GRID_HEIGHT // 2, colors['player'])
        self.ai_snake = Snake(3 * GRID_WIDTH // 4, GRID_HEIGHT // 2, colors['ai'])
        self.ai = SnakeAI(self.ai_snake, self.player, self.menu.difficulty_options[self.menu.current_difficulty])
        self.apple = self.spawn_apple()
        self.game_over = False
        self.winner = None
        self.game_started = False
        self.power_ups = []
        self.player_effects = []
        self.ai_effects = []
        if self.menu.special_abilities_enabled:
            self.spawn_power_up()

    def spawn_apple(self):
        while True:
            apple = (random.randint(2, GRID_WIDTH-3), 
                    random.randint(2, GRID_HEIGHT-3))
            if (apple not in self.player.body and 
                (not hasattr(self, 'ai_snake') or apple not in self.ai_snake.body)):
                return apple

    def spawn_power_up(self):
        if len(self.power_ups) < 2:  # Maximum 2 power-ups at a time
            new_power_up = PowerUp()  # Now PowerUp only creates freeze power-ups
            while (new_power_up.position in self.player.body or 
                   new_power_up.position in self.ai_snake.body or 
                   new_power_up.position == self.apple):
                new_power_up.spawn()
            self.power_ups.append(new_power_up)

    def get_snake_speed(self):
        base_speeds = [3, 5, 8]  # Slow, Normal, Fast
        base_speed = base_speeds[self.menu.current_speed]

        # Only check for freeze effect
        for effect in self.player_effects:
            if effect.remaining > 0:  # If frozen
                base_speed = 0

        return int(base_speed)

    def get_ai_speed(self):
        base_speeds = [3, 5, 8]  # Slow, Normal, Fast
        base_speed = base_speeds[self.menu.current_speed]

        # Only check for freeze effect
        for effect in self.ai_effects:
            if effect.remaining > 0:  # If frozen
                base_speed = 0

        return int(base_speed)

    def update_effects(self):
        self.player_effects = [effect for effect in self.player_effects if effect.update()]
        self.ai_effects = [effect for effect in self.ai_effects if effect.update()]

    def draw_walls(self):
        wall_color = self.menu.get_current_colors()['wall']
        wall_thickness = GRID_SIZE * 2
        pygame.draw.rect(self.screen, wall_color, (0, 0, WINDOW_WIDTH, wall_thickness))
        pygame.draw.rect(self.screen, wall_color, (0, WINDOW_HEIGHT - wall_thickness, WINDOW_WIDTH, wall_thickness))
        pygame.draw.rect(self.screen, wall_color, (0, 0, wall_thickness, WINDOW_HEIGHT))
        pygame.draw.rect(self.screen, wall_color, (WINDOW_WIDTH - wall_thickness, 0, wall_thickness, WINDOW_HEIGHT))

    def run(self):
        state = "menu"
        selected_option = 0
        target_apples = 10
        vs_ai = False
        color_selection_item = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if state == "menu":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            selected_option = (selected_option - 1) % 4
                        elif event.key == pygame.K_DOWN:
                            selected_option = (selected_option + 1) % 4
                        elif event.key == pygame.K_RETURN:
                            if selected_option == 0:  # Single Player
                                vs_ai = False
                                state = "select_speed"
                            elif selected_option == 1:  # VS AI
                                vs_ai = True
                                state = "select_difficulty"
                            elif selected_option == 2:  # Customize Colors
                                state = "customize_colors"
                                color_selection_item = 0
                            elif selected_option == 3:  # Quit
                                pygame.quit()
                                return

                elif state == "customize_colors":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            color_selection_item = (color_selection_item - 1) % 5
                        elif event.key == pygame.K_DOWN:
                            color_selection_item = (color_selection_item + 1) % 5
                        elif event.key == pygame.K_LEFT:
                            if color_selection_item < 4:  # Not on "Done"
                                color_type = ['background', 'player', 'ai', 'wall'][color_selection_item]
                                self.menu.current_colors[color_type] = (
                                    self.menu.current_colors[color_type] - 1
                                ) % len(self.menu.color_options[color_type])
                        elif event.key == pygame.K_RIGHT:
                            if color_selection_item < 4:  # Not on "Done"
                                color_type = ['background', 'player', 'ai', 'wall'][color_selection_item]
                                self.menu.current_colors[color_type] = (
                                    self.menu.current_colors[color_type] + 1
                                ) % len(self.menu.color_options[color_type])
                        elif event.key == pygame.K_RETURN and color_selection_item == 4:  # Done
                            state = "menu"

                elif state == "select_difficulty":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.menu.current_difficulty = (self.menu.current_difficulty - 1) % 3
                        elif event.key == pygame.K_DOWN:
                            self.menu.current_difficulty = (self.menu.current_difficulty + 1) % 3
                        elif event.key == pygame.K_RETURN:
                            state = "select_special_abilities"

                elif state == "select_special_abilities":
                    if event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_UP, pygame.K_DOWN]:
                            self.menu.special_abilities_enabled = not self.menu.special_abilities_enabled
                        elif event.key == pygame.K_RETURN:
                            state = "select_speed"

                elif state == "select_speed":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.menu.current_speed = (self.menu.current_speed - 1) % 3
                        elif event.key == pygame.K_DOWN:
                            self.menu.current_speed = (self.menu.current_speed + 1) % 3
                        elif event.key == pygame.K_RETURN:
                            state = "select_apples"

                elif state == "select_apples":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            target_apples = min(target_apples + 1, 50)
                        elif event.key == pygame.K_DOWN:
                            target_apples = max(target_apples - 1, 1)
                        elif event.key == pygame.K_RETURN:
                            self.reset_game()
                            state = "game"

                elif state == "game":
                    if event.type == pygame.KEYDOWN:
                        if not self.game_started and event.key == pygame.K_RETURN:
                            self.game_started = True
                        elif not self.game_over and self.game_started:
                            if event.key == pygame.K_UP:
                                self.player.change_direction(UP)
                            elif event.key == pygame.K_DOWN:
                                self.player.change_direction(DOWN)
                            elif event.key == pygame.K_LEFT:
                                self.player.change_direction(LEFT)
                            elif event.key == pygame.K_RIGHT:
                                self.player.change_direction(RIGHT)
                        if event.key == pygame.K_ESCAPE:
                            state = "menu"
                            selected_option = 0
                            self.reset_game()

            if state == "menu":
                self.menu.draw(self.screen, selected_option)
            elif state == "customize_colors":
                self.menu.draw_color_selector(self.screen, color_selection_item)
                preview_size = 40
                colors = self.menu.get_current_colors()
                for i, (key, color) in enumerate(colors.items()):
                    if i < 4:  # Skip if on "Done"
                        pygame.draw.rect(self.screen, color,
                                       (WINDOW_WIDTH//4*3, 250 + i * 60,
                                        preview_size, preview_size))
            elif state == "select_difficulty":
                self.menu.draw_difficulty_selector(self.screen)
            elif state == "select_special_abilities":
                self.menu.draw_special_abilities_selector(self.screen)
            elif state == "select_speed":
                self.menu.draw_speed_selector(self.screen)
            elif state == "select_apples":
                self.menu.draw_win_condition_selector(self.screen, target_apples)
            elif state == "game":
                self.screen.fill(self.menu.get_current_colors()['background'])
                self.draw_walls()

                if not self.game_started:
                    start_text = pygame.font.Font(None, 48).render("Press Enter to Start", True, WHITE)
                    text_rect = start_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                    self.screen.blit(start_text, text_rect)
                else:
                    if not self.game_over:
                        self.frame_count += 1
                        self.update_effects()

                        snake_speed = self.get_snake_speed()
                        if snake_speed > 0 and self.frame_count >= FPS // snake_speed:
                            self.player.move()

                            if vs_ai:
                                ai_speed = self.get_ai_speed()
                                if ai_speed > 0:
                                    ai_direction = self.ai.get_next_move(self.apple)
                                    self.ai_snake.change_direction(ai_direction)
                                    self.ai_snake.move()

                            self.frame_count = 0

                        if self.player.check_collision(self.ai_snake if vs_ai else None):
                            self.game_over = True
                            self.winner = "AI" if vs_ai else None
                        elif vs_ai and self.ai_snake.check_collision(self.player):
                            self.game_over = True
                            self.winner = "Player"

                        if self.player.body[0] == self.apple:
                            self.player.grow()
                            self.apple = self.spawn_apple()
                            if self.menu.special_abilities_enabled:
                                if random.random() < 0.3:  # 30% chance to spawn power-up
                                    self.spawn_power_up()
                        elif vs_ai and self.ai_snake.body[0] == self.apple:
                            self.ai_snake.grow()
                            self.apple = self.spawn_apple()
                            if self.menu.special_abilities_enabled:
                                if random.random() < 0.3:  # 30% chance to spawn power-up
                                    self.spawn_power_up()

                        # Check power-up collection
                        if self.menu.special_abilities_enabled:
                            for power_up in self.power_ups[:]:
                                if self.player.body[0] == power_up.position:
                                    # Player gets power-up, freeze AI
                                    self.ai_effects.append(PowerUpEffect())
                                    self.power_ups.remove(power_up)
                                elif vs_ai and self.ai_snake.body[0] == power_up.position:
                                    # AI gets power-up, freeze player
                                    self.player_effects.append(PowerUpEffect())
                                    self.power_ups.remove(power_up)

                        if self.player.score >= target_apples:
                            self.game_over = True
                            self.winner = "Player"
                        elif vs_ai and self.ai_snake.score >= target_apples:
                            self.game_over = True
                            self.winner = "AI"

                    self.player.draw(self.screen)
                    if vs_ai:
                        self.ai_snake.draw(self.screen)
                    pygame.draw.rect(self.screen, RED,
                                   (self.apple[0] * GRID_SIZE,
                                    self.apple[1] * GRID_SIZE,
                                    GRID_SIZE - 2,
                                    GRID_SIZE - 2))

                    if self.menu.special_abilities_enabled:
                        for power_up in self.power_ups:
                            power_up.draw(self.screen)

                    score_text = f"Player: {self.player.score}"
                    if vs_ai:
                        score_text += f" | AI: {self.ai_snake.score}"
                    score_surface = pygame.font.Font(None, 36).render(score_text, True, WHITE)
                    self.screen.blit(score_surface, (10, 10))

                    if self.game_over:
                        game_over_text = "Game Over! "
                        if self.winner == "Player":
                            game_over_text += "You win!"
                        elif self.winner == "AI":
                            game_over_text += "AI wins!"
                        else:
                            game_over_text += "You crashed!"
                        game_over_text += " Press ESC to return to menu"
                        text_surface = pygame.font.Font(None, 48).render(game_over_text, True, WHITE)
                        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                        self.screen.blit(text_surface, text_rect)

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()