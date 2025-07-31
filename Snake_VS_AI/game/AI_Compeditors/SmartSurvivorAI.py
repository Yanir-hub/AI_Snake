from game.ai import SnakeAI
from collections import deque
import random

class SmartSurvivorAI(SnakeAI):
    def get_next_move(self, apple_pos):
        head = self.snake.body[0]
        path = self.bfs(head, apple_pos)

        if path and len(path) >= 2:
            next_pos = path[1]
            # Dead-end avoidance: simulate flood fill from next_pos
            if self.flood_fill_area(next_pos) >= 15:
                direction = (next_pos[0] - head[0], next_pos[1] - head[1])
                if self.is_move_safe(direction):
                    return direction

        # Otherwise, go where there’s most open space
        return self.maximize_space()

    def bfs(self, start, goal):
        queue = deque([start])
        visited = {start: None}

        while queue:
            current = queue.popleft()
            if current == goal:
                path = []
                while current:
                    path.append(current)
                    current = visited[current]
                return path[::-1]

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited[neighbor] = current
                    queue.append(neighbor)

        return None

    def flood_fill_area(self, start):
        visited = set()
        queue = deque([start])
        area = 0

        while queue and area < 100:
            pos = queue.popleft()
            if pos in visited:
                continue
            visited.add(pos)
            area += 1

            for neighbor in self.get_neighbors(pos):
                if neighbor not in visited:
                    queue.append(neighbor)

        return area

    def maximize_space(self):
        head = self.snake.body[0]
        best_move = self.snake.direction
        max_area = -1

        for move in self.get_safe_moves():
            next_pos = (head[0] + move[0], head[1] + move[1])
            area = self.flood_fill_area(next_pos)
            if area > max_area:
                max_area = area
                best_move = move

        return best_move
