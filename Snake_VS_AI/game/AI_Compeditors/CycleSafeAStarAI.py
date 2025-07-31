from game.ai import SnakeAI
from heapq import heappush, heappop
from collections import deque
import random

class CycleSafeAStarAI(SnakeAI):
    def __init__(self, snake, opponent, difficulty='hard'):
        super().__init__(snake, opponent, difficulty)
        self.first_move_done = False

    def get_next_move(self, apple_pos):
        head = self.snake.body[0]

        if not self.first_move_done:
            self.first_move_done = True
            return self.get_direction_towards(head, apple_pos)

        path = self.a_star(head, apple_pos)
        if path and len(path) > 1:
            next_pos = path[1]
            if self.flood_fill_area(next_pos) >= len(self.snake.body):
                return (next_pos[0] - head[0], next_pos[1] - head[1])

        tail_path = self.a_star(head, self.snake.body[-1])
        if tail_path and len(tail_path) > 1:
            next_pos = tail_path[1]
            return (next_pos[0] - head[0], next_pos[1] - head[1])

        fallback = self.get_basic_direction(apple_pos)
        if self.is_move_safe(fallback):
            return fallback

        return self.get_safe_move()

    def get_direction_towards(self, start, target):
        dx = target[0] - start[0]
        dy = target[1] - start[1]
        if abs(dx) > abs(dy):
            return (1 if dx > 0 else -1, 0)
        elif dy != 0:
            return (0, 1 if dy > 0 else -1)
        return self.snake.direction

    def a_star(self, start, goal):
        open_set = []
        heappush(open_set, (self.heuristic(start, goal), 0, start, [start]))
        visited = set()

        while open_set:
            _, cost, current, path = heappop(open_set)
            if current == goal:
                return path
            if current in visited:
                continue
            visited.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    heappush(open_set, (
                        cost + 1 + self.heuristic(neighbor, goal),
                        cost + 1,
                        neighbor,
                        path + [neighbor]
                    ))
        return None

    def flood_fill_area(self, start):
        visited = set()
        queue = deque([start])
        area = 0

        while queue and area < 200:
            pos = queue.popleft()
            if pos in visited:
                continue
            visited.add(pos)
            area += 1
            for neighbor in self.get_neighbors(pos):
                if neighbor not in visited:
                    queue.append(neighbor)

        return area

    def get_safe_move(self):
        safe = self.get_safe_moves()
        if safe:
            return random.choice(safe)
        return self.snake.direction
