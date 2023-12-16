import numpy as np

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


if __name__ == "__main__":
    # with open("./day16/example_input", "r") as file:
    with open("./day16/input", "r") as file:
        grid = file.readlines()
    grid = np.array([[*row.strip()] for row in grid])
    energized_grid = np.array(
        [[EMPTY_SPACE for __ in range(grid.shape[1])] for _ in range(grid.shape[0])]
    )
    representation_grid = grid.copy()
    beams = [((0, 0), RIGHT)]
    state_memory = []
    while True:
        position, direction = beams.pop()
        energized_grid[position] = ENERGIZED
        representation_grid = draw_representation(
            position, direction, grid, representation_grid
        )
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
            representation_grid = draw_representation(
                position, direction, grid, representation_grid
            )
            direction, new_beam_direction = INTERACTION[(direction, grid[position])]
            if new_beam_direction and can_move(position, new_beam_direction, grid):
                beams.append(
                    (get_new_position(position, new_beam_direction), new_beam_direction)
                )
        if not beams:
            break
    with open("./day16/part1_output_representation", "w") as file:
        for row in representation_grid:
            file.write("".join(row) + "\n")
    print(
        f"Final number of tiles energized: {np.count_nonzero(energized_grid == ENERGIZED)}"
    )
