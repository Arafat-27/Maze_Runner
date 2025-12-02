def create_runner(x: int = 0, y: int = 0, orientation: str = "N"):
    return {"x": x, "y": y, "orientation": orientation}

def get_x(runner):
    return runner["x"]

def get_y(runner):
    return runner["y"]

def get_orientation(runner):
    return runner["orientation"]

def turn(runner, direction: str):
    orient = runner["orientation"]

    if direction == "Left":
        if orient == "N": runner["orientation"] = "W"
        elif orient == "W": runner["orientation"] = "S"
        elif orient == "S": runner["orientation"] = "E"
        elif orient == "E": runner["orientation"] = "N"

    elif direction == "Right":
        if orient == "N": runner["orientation"] = "E"
        elif orient == "E": runner["orientation"] = "S"
        elif orient == "S": runner["orientation"] = "W"
        elif orient == "W": runner["orientation"] = "N"

    return runner

def forward(runner):
    orientation = runner["orientation"]
    
    if orientation == "N":
        runner["y"] += 1  
    elif orientation == "E":
        runner["x"] += 1  
    elif orientation == "S":
        runner["y"] -= 1  
    elif orientation == "W":
        runner['x'] -= 1  

    return runner