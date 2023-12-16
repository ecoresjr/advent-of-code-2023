import numpy as np
import pandas as pd

RIGHT = (0, 1)
LEFT = (0, -1)
DOWN = (1, 0)
UP = (-1, 0)

REPRESENTATION = {RIGHT: ">", LEFT: "<", DOWN: "v", UP: "^"}

SLASH_MIRROR = "/"
BACKSLASH_MIRROR = "\\"
VERTICAL_SPLITTER = "|"
HORIZONTAL_SPLITTER = "-"
EMPTY_SPACE = "."
ENERGIZED = "#"

INTERACTION = {
    (RIGHT, SLASH_MIRROR): (UP, None),
    (LEFT, SLASH_MIRROR): (DOWN, None),
    (UP, SLASH_MIRROR): (RIGHT, None),
    (DOWN, SLASH_MIRROR): (LEFT, None),
    (RIGHT, BACKSLASH_MIRROR): (DOWN, None),
    (LEFT, BACKSLASH_MIRROR): (UP, None),
    (UP, BACKSLASH_MIRROR): (LEFT, None),
    (DOWN, BACKSLASH_MIRROR): (RIGHT, None),
    (LEFT, VERTICAL_SPLITTER): (UP, DOWN),
    (RIGHT, VERTICAL_SPLITTER): (UP, DOWN),
    (DOWN, VERTICAL_SPLITTER): (DOWN, None),
    (UP, VERTICAL_SPLITTER): (UP, None),
    (DOWN, HORIZONTAL_SPLITTER): (LEFT, RIGHT),
    (UP, HORIZONTAL_SPLITTER): (LEFT, RIGHT),
    (LEFT, HORIZONTAL_SPLITTER): (LEFT, None),
    (RIGHT, HORIZONTAL_SPLITTER): (RIGHT, None),
    (DOWN, EMPTY_SPACE): (DOWN, None),
    (UP, EMPTY_SPACE): (UP, None),
    (LEFT, EMPTY_SPACE): (LEFT, None),
    (RIGHT, EMPTY_SPACE): (RIGHT, None),
}


def draw_representation(position, direction, grid, representation_grid):
    if grid[position] == EMPTY_SPACE:
        representation = REPRESENTATION[direction]
        if representation_grid[position] != EMPTY_SPACE:
            representation = "2"
            if representation_grid[position].isdigit():
                representation = int(representation_grid[position]) + 1
        representation_grid[position] = representation
    return representation_grid


def can_move(position, direction, grid):
    return (
        not (position[1] == 0 and direction == LEFT)
        and not (position[0] == 0 and direction == UP)
        and not (position[1] == grid.shape[1] - 1 and direction == RIGHT)
        and not (position[0] == grid.shape[0] - 1 and direction == DOWN)
    )


def get_new_position(position, direction):
    return (position[0] + direction[0], position[1] + direction[1])


def load_grid(path_input):
    with open(path_input, "r") as file:
        grid = file.readlines()
    return np.array([[*row.strip()] for row in grid])


INPUT_GRID = load_grid("./day16/input")
# INPUT_GRID = load_grid("./day16/example_input")


def navigate_grid(start_configuration):
    grid = INPUT_GRID.copy()
    energized_grid = np.array(
        [[EMPTY_SPACE for __ in range(grid.shape[1])] for _ in range(grid.shape[0])]
    )
    beams = [(start_configuration["position"], start_configuration["direction"])]
    state_memory = []
    while True:
        position, direction = beams.pop()
        energized_grid[position] = ENERGIZED
        direction, new_beam_direction = INTERACTION[(direction, grid[position])]
        if new_beam_direction and can_move(position, new_beam_direction, grid):
            beams.append(
                (get_new_position(position, new_beam_direction), new_beam_direction)
            )
        while can_move(position, direction, grid):
            if (position, direction) in state_memory:
                break
            else:
                state_memory.append((position, direction))
            position = get_new_position(position, direction)
            energized_grid[position] = ENERGIZED
            direction, new_beam_direction = INTERACTION[(direction, grid[position])]
            if new_beam_direction and can_move(position, new_beam_direction, grid):
                beams.append(
                    (get_new_position(position, new_beam_direction), new_beam_direction)
                )
        if not beams:
            break
    return np.count_nonzero(energized_grid == ENERGIZED)


if __name__ == "__main__":
    start_configurations = []
    for i in range(INPUT_GRID.shape[0]):
        for j in range(INPUT_GRID.shape[1]):
            if i == 0:
                start_configurations.append({"position": (i, j), "direction": DOWN})
            if i == INPUT_GRID.shape[0] - 1:
                start_configurations.append({"position": (i, j), "direction": UP})
            if j == 0:
                start_configurations.append({"position": (i, j), "direction": RIGHT})
            if j == INPUT_GRID.shape[1] - 1:
                start_configurations.append({"position": (i, j), "direction": LEFT})
    start_configurations = pd.DataFrame(start_configurations)
    results = start_configurations.apply(navigate_grid, axis=1)
    print(f"Final number of tiles energized in the best configuration: {results.max()}")
