from typing import Tuple, Optional, List
from collections import deque

class Maze:
    def __init__(self, width: int = 5, height: int = 5):
        self._width = width
        self._height = height

        self.walls = []
        for y in range(height):
            row = []
            for x in range(width):
                cell_walls = {
                    "N": y == height - 1,
                    "S": y == 0,
                    "W": x == 0,
                    "E": x == width - 1,
                }
                row.append(cell_walls)
            self.walls.append(row)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def add_horizontal_wall(self, x_coordinate, horizontal_line):
        if 0 <= horizontal_line < self._height:
            self.walls[horizontal_line][x_coordinate]["S"] = True
            if horizontal_line > 0:
                self.walls[horizontal_line - 1][x_coordinate]["N"] = True

    def add_vertical_wall(self, y_coordinate, vertical_line):
        if 0 <= vertical_line < self._width:
            self.walls[y_coordinate][vertical_line]["W"] = True
            if vertical_line > 0:
                self.walls[y_coordinate][vertical_line - 1]["E"] = True

    def get_wall(self, x_coordinate: int, y_coordinate: int) -> Tuple[bool, bool, bool, bool]:
        cell = self.walls[y_coordinate][x_coordinate]
        return (cell["N"], cell["E"], cell["S"], cell["W"])

    def get_walls(self, x_coordinate: int, y_coordinate: int) -> Tuple[bool, bool, bool, bool]:
        return self.get_wall(x_coordinate, y_coordinate)

    def sense_walls(self, runner) -> Tuple[bool, bool, bool]:
        x = runner["x"]
        y = runner["y"]
        orientation = runner["orientation"]

        N, E, S, W = self.get_wall(x, y)

        if orientation == "N":
            return (W, N, E)
        elif orientation == "E":
            return (N, E, S)
        elif orientation == "S":
            return (E, S, W)
        elif orientation == "W":
            return (S, W, N)

    def go_straight(self, runner):
        x = runner["x"]
        y = runner["y"]
        orientation = runner["orientation"]

        N, E, S, W = self.get_wall(x, y)

        if orientation == "N":
            if N:
                raise ValueError("Wall in front")
            runner["y"] += 1
        elif orientation == "E":
            if E:
                raise ValueError("Wall in front")
            runner["x"] += 1
        elif orientation == "S":
            if S:
                raise ValueError("Wall in front")
            runner["y"] -= 1
        elif orientation == "W":
            if W:
                raise ValueError("Wall in front")
            runner["x"] -= 1

        return runner

    def turn_left(self, runner):
        orientations = ["N", "W", "S", "E"]
        runner["orientation"] = orientations[(orientations.index(runner["orientation"]) + 1) % 4]
        return runner

    def turn_right(self, runner):
        orientations = ["N", "E", "S", "W"]
        runner["orientation"] = orientations[(orientations.index(runner["orientation"]) + 1) % 4]
        return runner

    def turn_back(self, runner):
        orientations = ["N", "E", "S", "W"]
        runner["orientation"] = orientations[(orientations.index(runner["orientation"]) + 2) % 4]
        return runner

    def move(self, runner):
        left, front, right = self.sense_walls(runner)

        if not left:
            self.turn_left(runner)
            self.go_straight(runner)
            return runner, "LF"

        if not front:
            self.go_straight(runner)
            return runner, "F"

        if not right:
            self.turn_right(runner)
            self.go_straight(runner)
            return runner, "RF"

        self.turn_back(runner)
        self.go_straight(runner)
        return runner, "RRF"

    def explore(self, runner, goal: Optional[Tuple[int, int]] = None) -> str:
        if goal is None:
            goal = (self._width - 1, self._height - 1)

        actions = ""
        max_steps = self._width * self._height * 4
        steps = 0

        while (runner["x"], runner["y"]) != goal and steps < max_steps:
            runner, step_actions = self.move(runner)
            actions += step_actions
            steps += 1

        return actions

    def shortest_path(
        self,
        starting: Optional[Tuple[int, int]] = None,
        goal: Optional[Tuple[int, int]] = None
    ) -> List[Tuple[int, int]]:

        if starting is None:
            starting = (0, 0)

        if goal is None:
            goal = (self._width - 1, self._height - 1)

        queue = deque([starting])
        visited = {starting}
        parent = {starting: None}

        while queue:
            current = queue.popleft()
            x, y = current

            if current == goal:
                break

            N, E, S, W = self.get_wall(x, y)

            neighbors = []
            if not N and y < self._height - 1:
                neighbors.append((x, y + 1))
            if not E and x < self._width - 1:
                neighbors.append((x + 1, y))
            if not S and y > 0:
                neighbors.append((x, y - 1))
            if not W and x > 0:
                neighbors.append((x - 1, y))

            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        path = []
        current = goal

        while current is not None:
            path.append(current)
            current = parent.get(current)

        path.reverse()
        return path
