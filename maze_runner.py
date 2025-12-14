import argparse
import sys
from typing import Tuple
from maze import Maze
from runner import create_runner


def maze_reader(maze_file: str) -> Maze:
    try:
        with open(maze_file, "r") as f:
            raw_lines = [line.rstrip("\n") for line in f if line.strip()]
    except Exception:
        raise IOError("Cannot read maze file")

    if not raw_lines:
        raise ValueError("Invalid maze")

    max_len = max(len(line) for line in raw_lines)

    if max_len < 3 or len(raw_lines) < 3:
        raise ValueError("Invalid maze")

    if max_len % 2 == 0 or len(raw_lines) % 2 == 0:
        raise ValueError("Invalid maze dimensions")

    lines = [line.ljust(max_len, "#") for line in raw_lines]

    width = (max_len - 1) // 2
    height = (len(lines) - 1) // 2

    maze = Maze(width, height)

    for y in range(height + 1):
        line = lines[2 * y]
        for x in range(width):
            if line[2 * x + 1] == "#":
                if y < height:
                    maze.add_horizontal_wall(x, y)

    for y in range(height):
        line = lines[2 * y + 1]
        for x in range(width + 1):
            if line[2 * x] == "#":
                if x < width:
                    maze.add_vertical_wall(y, x)

    return maze


def parse_position(value: str, maze: Maze) -> Tuple[int, int]:
    x, y = map(int, value.split(","))
    return x, y


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("maze")
    args = parser.parse_args()

    try:
        maze = maze_reader(args.maze)
        runner = create_runner(0, 0, "N")

        while True:
            runner, _ = maze.move(runner)

    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()