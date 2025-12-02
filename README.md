# Maze Runner

This project implements a grid-based maze with a runner that can explore the maze using a left-hug navigation algorithm and compute the shortest path between two positions.

The system supports:
- Maze creation with configurable width and height  
- Automatic external wall generation  
- Internal horizontal and vertical walls  
- Wall sensing relative to runner direction (Left, Front, Right)  
- Runner movement and exploration  
- Shortest path calculation using Breadth-First Search (BFS)  

## Project Structure

src/
├── maze.py
├── runner.py
└── maze_runner.py

tests/
├── test_maze.py
├── test_runner.py
├── test_maze_runner.py
├── test_maze_reader.py
└── test_shortest_path.py

## How to Run the Tests

From the project root directory:

```bash
pytest
or

bash
Copy code
python -m pytest
To run a specific test file:

bash
Copy code
pytest test_maze.py
pytest test_shortest_path.py
Example Usage
python
Copy code
from src.maze import Maze

maze = Maze(5, 5)
maze.add_horizontal_wall(2, 2)
maze.add_vertical_wall(1, 3)

runner = {"x": 0, "y": 0, "orientation": "E"}

exploration_path = maze.explore(runner)
shortest = maze.shortest_path()

print("Exploration:", exploration_path)
print("Shortest path:", shortest)
Algorithms Used
Left-Hug Wall-Following Algorithm for exploration

Breadth-First Search (BFS) for shortest path calculation

Author
Abdullah