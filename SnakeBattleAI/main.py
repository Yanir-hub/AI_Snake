import pygame
import random
from game.constants import *
from game.snake import Snake
from game.ai import SnakeAI
from game.menu import Menu

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
        self.player = Snake(GRID_WIDTH // 4, GRID_HEIGHT // 2, GREEN)
        self.ai_snake = Snake(3 * GRID_WIDTH // 4, GRID_HEIGHT // 2, BLUE)
        self.ai = SnakeAI(self.ai_snake, self.player, self.menu.difficulty_options[self.menu.current_difficulty])
        self.apple = self.spawn_apple()
        self.game_over = False
        self.winner = None

    def spawn_apple(self):
        while True:
            # Spawn apple only in the playable area (2 cells away from walls due to thicker walls)
            apple = (random.randint(2, GRID_WIDTH-3), 
                    random.randint(2, GRID_HEIGHT-3))
            if (apple not in self.player.body and 
                (not hasattr(self, 'ai_snake') or apple not in self.ai_snake.body)):
                return apple

    def get_snake_speed(self):
        speeds = [3, 5, 8]  # Slow, Normal, Fast
        return speeds[self.menu.current_speed]

    def draw_walls(self):
        BROWN = (139, 69, 19)  # Define brown color
        wall_thickness = GRID_SIZE * 2  # Make walls two grid cells thick

        # Draw top wall
        pygame.draw.rect(self.screen, BROWN, (0, 0, WINDOW_WIDTH, wall_thickness))
        # Draw bottom wall
        pygame.draw.rect(self.screen, BROWN, (0, WINDOW_HEIGHT - wall_thickness, WINDOW_WIDTH, wall_thickness))
        # Draw left wall
        pygame.draw.rect(self.screen, BROWN, (0, 0, wall_thickness, WINDOW_HEIGHT))
        # Draw right wall
        pygame.draw.rect(self.screen, BROWN, (WINDOW_WIDTH - wall_thickness, 0, wall_thickness, WINDOW_HEIGHT))

    def run(self):
        state = "menu"
        selected_option = 0
        target_apples = 10
        vs_ai = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if state == "menu":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            selected_option = (selected_option - 1) % 3
                        elif event.key == pygame.K_DOWN:
                            selected_option = (selected_option + 1) % 3
                        elif event.key == pygame.K_RETURN:
                            if selected_option == 0:  # Single Player
                                vs_ai = False
                                state = "select_speed"
                            elif selected_option == 1:  # VS AI
                                vs_ai = True
                                state = "select_difficulty"
                            elif selected_option == 2:  # Quit
                                pygame.quit()
                                return

                elif state == "select_difficulty":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.menu.current_difficulty = (self.menu.current_difficulty - 1) % 3
                        elif event.key == pygame.K_DOWN:
                            self.menu.current_difficulty = (self.menu.current_difficulty + 1) % 3
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
                        if not self.game_over:
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
            elif state == "select_difficulty":
                self.menu.draw_difficulty_selector(self.screen)
            elif state == "select_speed":
                self.menu.draw_speed_selector(self.screen)
            elif state == "select_apples":
                self.menu.draw_win_condition_selector(self.screen, target_apples)
            elif state == "game":
                # Game logic
                if not self.game_over:
                    self.frame_count += 1
                    snake_speed = self.get_snake_speed()
                    if self.frame_count >= FPS // snake_speed:
                        # Move player
                        self.player.move()

                        # Move AI if vs_ai mode
                        if vs_ai:
                            ai_direction = self.ai.get_next_move(self.apple)
                            self.ai_snake.change_direction(ai_direction)
                            self.ai_snake.move()

                        self.frame_count = 0

                    # Check collisions
                    if self.player.check_collision(self.ai_snake if vs_ai else None):
                        self.game_over = True
                        self.winner = "AI" if vs_ai else None
                    elif vs_ai and self.ai_snake.check_collision(self.player):
                        self.game_over = True
                        self.winner = "Player"

                    # Check apple collection
                    if self.player.body[0] == self.apple:
                        self.player.grow()
                        self.apple = self.spawn_apple()
                    elif vs_ai and self.ai_snake.body[0] == self.apple:
                        self.ai_snake.grow()
                        self.apple = self.spawn_apple()

                    # Check win condition
                    if self.player.score >= target_apples:
                        self.game_over = True
                        self.winner = "Player"
                    elif vs_ai and self.ai_snake.score >= target_apples:
                        self.game_over = True
                        self.winner = "AI"

                # Draw game
                self.screen.fill(BLACK)
                self.draw_walls()  # Draw the walls first
                self.player.draw(self.screen)
                if vs_ai:
                    self.ai_snake.draw(self.screen)
                pygame.draw.rect(self.screen, RED,
                               (self.apple[0] * GRID_SIZE,
                                self.apple[1] * GRID_SIZE,
                                GRID_SIZE - 2,
                                GRID_SIZE - 2))

                # Draw scores
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