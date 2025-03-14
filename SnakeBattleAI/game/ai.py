from game.constants import *
import heapq
import random

class SnakeAI:
    def __init__(self, snake, target, difficulty='medium'):
        self.snake = snake
        self.target = target
        self.difficulty = difficulty
        self.last_direction = None

    def get_next_move(self, apple_pos):
        if self.difficulty == 'easy':
            return self.get_easy_move(apple_pos)
        elif self.difficulty == 'medium':
            return self.get_medium_move(apple_pos)
        else:  # hard
            return self.get_hard_move(apple_pos)

    def get_easy_move(self, apple_pos):
        # Simple movement with 30% random direction
        if random.random() < 0.3:
            safe_moves = self.get_safe_moves()
            return random.choice(safe_moves) if safe_moves else self.snake.direction

        return self.get_basic_direction(apple_pos)

    def get_medium_move(self, apple_pos):
        head = self.snake.body[0]

        # Get all possible next positions
        possible_moves = self.get_safe_moves()
        if not possible_moves:
            return self.snake.direction

        best_move = None
        best_score = float('-inf')

        for move in possible_moves:
            next_pos = (head[0] + move[0], head[1] + move[1])

            # Calculate score for this move
            score = 0

            # Distance to apple (negative because closer is better)
            apple_distance = self.heuristic(next_pos, apple_pos)
            score -= apple_distance * 2

            # Avoid walls - give higher scores to moves away from walls
            if next_pos[0] > 0 and next_pos[0] < GRID_WIDTH - 1:
                score += 3
            if next_pos[1] > 0 and next_pos[1] < GRID_HEIGHT - 1:
                score += 3

            # Look ahead for available moves from next position
            future_moves = len(self.get_neighbors((next_pos[0], next_pos[1])))
            score += future_moves * 2

            # Add some randomness to avoid predictable movement
            score += random.uniform(0, 2)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move if best_move else self.snake.direction

    def get_hard_move(self, apple_pos):
        head = self.snake.body[0]

        # Get all possible next positions
        possible_moves = self.get_safe_moves()
        if not possible_moves:
            return self.snake.direction

        best_move = None
        best_score = float('-inf')

        for move in possible_moves:
            next_pos = (head[0] + move[0], head[1] + move[1])
            score = self.evaluate_move(next_pos, apple_pos)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move if best_move else self.get_safe_move()

    def evaluate_move(self, pos, apple_pos):
        score = 0

        # Distance to apple (negative because closer is better)
        apple_distance = self.heuristic(pos, apple_pos)
        score -= apple_distance * 2

        # Check if move blocks opponent
        if self.target and len(self.target.body) > 0:
            opponent_head = self.target.body[0]
            opponent_to_apple = self.heuristic(opponent_head, apple_pos)

            # If we're closer to apple, prioritize getting it
            if apple_distance < opponent_to_apple:
                score += 50

            # Bonus for blocking opponent's path to apple
            if self.is_blocking_opponent(pos, opponent_head, apple_pos):
                score += 30

            # Bonus for limiting opponent's moves
            opponent_moves = len(self.get_neighbors(opponent_head))
            if opponent_moves <= 2:
                score += 20

        # Penalize moves that limit our own mobility
        our_moves = len(self.get_neighbors(pos))
        score += our_moves * 5

        return score

    def is_blocking_opponent(self, our_pos, opponent_pos, apple_pos):
        # Check if our position is between opponent and apple
        return (self.heuristic(opponent_pos, our_pos) + 
                self.heuristic(our_pos, apple_pos) <=
                self.heuristic(opponent_pos, apple_pos) + 1)

    def get_safe_moves(self):
        safe_moves = []
        head = self.snake.body[0]
        for direction in [UP, DOWN, LEFT, RIGHT]:
            if self.is_move_safe(direction):
                safe_moves.append(direction)
        return safe_moves

    def is_move_safe(self, direction):
        head = self.snake.body[0]
        new_pos = (head[0] + direction[0], head[1] + direction[1])
        return self.is_position_safe(new_pos)

    def is_position_safe(self, pos):
        # Modified to include edges (0 and max values)
        return (0 <= pos[0] <= GRID_WIDTH - 1 and 
                0 <= pos[1] <= GRID_HEIGHT - 1 and 
                pos not in self.snake.body and
                (not self.target or pos not in self.target.body))

    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        for dx, dy in [UP, DOWN, LEFT, RIGHT]:
            new_x, new_y = x + dx, y + dy
            if self.is_position_safe((new_x, new_y)):
                neighbors.append((new_x, new_y))
        return neighbors

    def get_basic_direction(self, target):
        head = self.snake.body[0]
        dx = target[0] - head[0]
        dy = target[1] - head[1]

        if abs(dx) > abs(dy):
            direction = (1 if dx > 0 else -1, 0)
        else:
            direction = (0, 1 if dy > 0 else -1)

        if self.is_move_safe(direction):
            return direction
        return self.get_safe_move()

    def find_path(self, start, goal):
        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == goal:
                break

            for next_pos in self.get_neighbors(current):
                new_cost = cost_so_far[current] + 1

                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + self.heuristic(goal, next_pos)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current

        if goal not in came_from:
            return None

        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_direction_to(self, current, target):
        dx = target[0] - current[0]
        dy = target[1] - current[1]

        # Ensure we only move one step at a time
        if abs(dx) >= abs(dy):
            return (1 if dx > 0 else -1, 0) if dx != 0 else (0, 1 if dy > 0 else -1)
        else:
            return (0, 1 if dy > 0 else -1)

    def get_safe_move(self):
        safe_moves = self.get_safe_moves()
        if safe_moves:
            return random.choice(safe_moves)
        return self.snake.direction