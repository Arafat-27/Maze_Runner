import matplotlib.pyplot as plt
from maze_runner import maze_reader
from runner import create_runner


def draw_maze(ax, maze):
    c, w = "#cccccc", 0.5
    for y in range(maze.height):
        for x in range(maze.width):
            N, E, S, W = maze.get_walls(x, y)
            if N: ax.plot([x, x + 1], [y + 1, y + 1], c, lw=w)
            if S: ax.plot([x, x + 1], [y, y], c, lw=w)
            if W: ax.plot([x, x], [y, y + 1], c, lw=w)
            if E: ax.plot([x + 1, x + 1], [y, y + 1], c, lw=w)


def animate(maze_file, goal_x=None, goal_y=None):
    plt.ion()
    maze = maze_reader(maze_file)
    
    start_x, start_y = 0, maze.height - 1
    goal_x = goal_x if goal_x is not None else maze.width // 2
    goal_y = goal_y if goal_y is not None else maze.height // 2
    
    runner = create_runner(start_x, start_y, "E")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor("#0e0e0e")
    ax.set_facecolor("#0e0e0e")
    ax.set_aspect("equal")
    ax.set_xlim(0, maze.width)
    ax.set_ylim(0, maze.height)
    ax.invert_yaxis()
    ax.axis("off")
    
    draw_maze(ax, maze)
    
    goal_center = (goal_x + 0.5, goal_y + 0.5)
    goal_patches = [
        ax.add_patch(plt.Circle(goal_center, r, color="#ffaa00", alpha=a))
        for r, a in [(0.55, 0.15), (0.45, 0.25), (0.35, 0.8)]
    ]
    
    xs, ys = [], []
    path_line, = ax.plot([], [], color="#00ffd5", lw=1.2)
    runner_dot, = ax.plot([], [], "o", color="#ff3355", markersize=4)
    
    max_steps = maze.width * maze.height * 4
    
    for step in range(max_steps):
        x, y = runner["x"], runner["y"]
        px, py = x + 0.5, y + 0.5
        
        xs.append(px)
        ys.append(py)
        path_line.set_data(xs, ys)
        runner_dot.set_data([px], [py])
        
        fig.canvas.draw_idle()
        plt.pause(0.06)
        
        if (x, y) == (goal_x, goal_y):
            for circle in goal_patches:
                circle.set_color("#00ff66")
                circle.set_alpha(0.9)
            break
        
        runner, _ = maze.move(runner)
    
    plt.ioff()
    plt.show()

animate("demo_maze.mz")