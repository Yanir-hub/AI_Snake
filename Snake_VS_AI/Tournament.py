import pygame
import random
from game.constants import *
from game.snake import Snake
from game.ai import SnakeAI

from game.AI_Compeditors.CycleSafeAStarAI import CycleSafeAStarAI
from game.AI_Compeditors.PathfindingStrategicAI import PathfindingStrategicAI
from game.AI_Compeditors.SmartSurvivorAI import SmartSurvivorAI
from game.AI_Compeditors.UltimateHybridAI import UltimateHybridAI


# Alternate AI for comparison (optional)
class AlternateAI(SnakeAI):
    def get_next_move(self, apple_pos):
        return self.get_basic_direction(apple_pos)

def spawn_apple(snake1, snake2):
    while True:
        pos = (random.randint(2, GRID_WIDTH - 3), random.randint(2, GRID_HEIGHT - 3))
        if pos not in snake1.body and pos not in snake2.body:
            return pos

def simulate_game(screen, clock, AI1_class, AI2_class, max_apples=10, fps=30, headless=False):
    snake1 = Snake(GRID_WIDTH // 4, GRID_HEIGHT // 2, (0, 255, 0))
    snake2 = Snake(3 * GRID_WIDTH // 4, GRID_HEIGHT // 2, (0, 0, 255))
    ai1 = AI1_class(snake1, snake2, difficulty='hard')
    ai2 = AI2_class(snake2, snake1, difficulty='hard')

    apple = spawn_apple(snake1, snake2)

    # Fix: Set initial direction toward apple to avoid blocked reversal
    dx1 = apple[0] - snake1.body[0][0]
    dy1 = apple[1] - snake1.body[0][1]
    if abs(dx1) > abs(dy1):
        snake1.direction = (1 if dx1 > 0 else -1, 0)
    elif dy1 != 0:
        snake1.direction = (0, 1 if dy1 > 0 else -1)

    dx2 = apple[0] - snake2.body[0][0]
    dy2 = apple[1] - snake2.body[0][1]
    if abs(dx2) > abs(dy2):
        snake2.direction = (1 if dx2 > 0 else -1, 0)
    elif dy2 != 0:
        snake2.direction = (0, 1 if dy2 > 0 else -1)

    while True:
        if not headless:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        dir1 = ai1.get_next_move(apple)
        snake1.change_direction(dir1)
        snake1.move()

        dir2 = ai2.get_next_move(apple)
        snake2.change_direction(dir2)
        snake2.move()

        if snake1.body[0] == apple:
            snake1.grow()
            apple = spawn_apple(snake1, snake2)
        elif snake2.body[0] == apple:
            snake2.grow()
            apple = spawn_apple(snake1, snake2)

        if snake1.check_collision(snake2):
            return "AI2"
        elif snake2.check_collision(snake1):
            return "AI1"
        elif snake1.score >= max_apples:
            return "AI1"
        elif snake2.score >= max_apples:
            return "AI2"

        if not headless:
            screen.fill((0, 0, 0))
            draw_walls(screen)
            snake1.draw(screen)
            snake2.draw(screen)

            pygame.draw.rect(screen, RED,
                             (apple[0]*GRID_SIZE, apple[1]*GRID_SIZE, GRID_SIZE-2, GRID_SIZE-2))

            pygame.display.flip()
            clock.tick(fps)



def draw_walls(screen):
    wall_color = (139, 69, 19)
    thickness = GRID_SIZE * 2
    pygame.draw.rect(screen, wall_color, (0, 0, WINDOW_WIDTH, thickness))
    pygame.draw.rect(screen, wall_color, (0, WINDOW_HEIGHT - thickness, WINDOW_WIDTH, thickness))
    pygame.draw.rect(screen, wall_color, (0, 0, thickness, WINDOW_HEIGHT))
    pygame.draw.rect(screen, wall_color, (WINDOW_WIDTH - thickness, 0, thickness, WINDOW_HEIGHT))

def run_tournament(rounds=100, headless=False):
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) if not headless else None
    pygame.display.set_caption("Snake AI Tournament")
    clock = pygame.time.Clock()

    wins = {"AI1": 0, "AI2": 0}
    font = pygame.font.Font(None, 36) if not headless else None

    for i in range(rounds):
        if not headless:
            screen.fill((0, 0, 0))
            title = font.render(f"Round {i+1} / {rounds}", True, (255, 255, 255))
            screen.blit(title, (10, 10))
            pygame.display.flip()
            pygame.time.delay(300)

        #PUT HERE THE SNAKE YOUR SNAKE COMPETES WITH
        #AI1 ->>>>>>>>>>>>> AI2

        winner = simulate_game(screen, clock, SnakeAI, PathfindingStrategicAI, headless=headless)
        wins[winner] += 1
        print(f"Round {i+1}: {winner} wins")

        if not headless:
            pygame.time.delay(500)

    pygame.quit()
    print("\n--- Tournament Results ---")
    print("SnakeAI Wins:", wins["AI1"])
    print("Compeditor Wins:", wins["AI2"])

if __name__ == "__main__":
    run_tournament(rounds=100, headless=True)  # Change headless=False to see visuals
