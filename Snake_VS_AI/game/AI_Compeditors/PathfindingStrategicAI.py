from game.ai import SnakeAI
from game.constants import *
from collections import deque
import random

class PathfindingStrategicAI(SnakeAI):
    def get_next_move(self, apple_pos):
        head = self.snake.body[0]
        path = self.bfs(head, apple_pos)

        if path and len(path) >= 2:
            next_pos = path[1]
            direction = (next_pos[0] - head[0], next_pos[1] - head[1])
            if self.is_move_safe(direction):
                return direction

        # No safe path: fallback to high-mobility move
        return self.get_mobility_fallback()

    def bfs(self, start, goal):
        queue = deque([start])
        visited = {start: None}

        while queue:
            current = queue.popleft()

            if current == goal:
                # Reconstruct path
                path = []
                while current:
                    path.append(current)
                    current = visited[current]
                return path[::-1]

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited[neighbor] = current
                    queue.append(neighbor)

        return None  # No path

    def get_mobility_fallback(self):
        head = self.snake.body[0]
        best_move = self.snake.direction
        max_future = -1

        for move in self.get_safe_moves():
            next_pos = (head[0] + move[0], head[1] + move[1])
            future_options = len(self.get_neighbors(next_pos))
            score = future_options

            # Bias toward center to avoid edge traps
            score += -abs(next_pos[0] - (GRID_WIDTH // 2)) * 0.1
            score += -abs(next_pos[1] - (GRID_HEIGHT // 2)) * 0.1

            if score > max_future:
                max_future = score
                best_move = move

        return best_move
