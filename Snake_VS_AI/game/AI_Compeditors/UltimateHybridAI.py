from game.ai import SnakeAI
from heapq import heappush, heappop
from collections import deque
import random

class UltimateHybridAI(SnakeAI):
    def get_next_move(self, apple_pos):
        head = self.snake.body[0]

        path_to_apple = self.a_star(head, apple_pos)
        if path_to_apple and len(path_to_apple) > 1:
            next_pos = path_to_apple[1]
            if self.safe_area(next_pos) > len(self.snake.body) * 1.1:
                return (next_pos[0] - head[0], next_pos[1] - head[1])

        path_to_tail = self.a_star(head, self.snake.body[-1])
        if path_to_tail and len(path_to_tail) > 1:
            return (path_to_tail[1][0] - head[0], path_to_tail[1][1] - head[1])

        # FIXED: move safely toward apple if possible
        return self.get_basic_direction(apple_pos)

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

    def safe_area(self, start):
        visited = set()
        queue = deque([start])
        area = 0
        while queue:
            pos = queue.popleft()
            if pos in visited:
                continue
            visited.add(pos)
            area += 1
            for neighbor in self.get_neighbors(pos):
                if neighbor not in visited:
                    queue.append(neighbor)
        return area

    def get_basic_direction(self, target):
        head = self.snake.body[0]
        dx = target[0] - head[0]
        dy = target[1] - head[1]

        if abs(dx) > abs(dy):
            primary = (1 if dx > 0 else -1, 0)
            secondary = (0, 1 if dy > 0 else -1)
        else:
            primary = (0, 1 if dy > 0 else -1)
            secondary = (1 if dx > 0 else -1, 0)

        for direction in [primary, secondary]:
            if self.is_move_safe(direction):
                return direction

        return self.get_safe_move()

    def get_safe_move(self):
        safe_moves = self.get_safe_moves()
        if safe_moves:
            return random.choice(safe_moves)
        return self.snake.direction
