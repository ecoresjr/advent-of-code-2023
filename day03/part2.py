import numpy as np

EMPTY_SPACE = "."
GEAR = "*"


def next_position(position, shape):
    position = (position[0], position[1] + 1)
    if position[1] == shape[1]:
        position = (position[0] + 1, 0)
    if position[0] == shape[0]:
        position = None
    return position


def find_next_number(schematic, position):
    start_position = None
    end_position = None
    number = []
    while not schematic[position].isdigit():
        position = next_position(position, schematic.shape)
        if not position:
            return None, None, None
    start_position = position
    while schematic[position].isdigit():
        number.append(schematic[position])
        end_position = position
        position = next_position(position, schematic.shape)
        if not position or position[0] != start_position[0]:
            break
    return int("".join(number)) if number else None, start_position, end_position


def find_adjacent_gears(start_position, end_position, schematic, gears, number):
    top = start_position[0] - 1 if start_position[0] > 0 else start_position[0]
    bottom = (
        start_position[0] + 1
        if start_position[0] < schematic.shape[0] - 1
        else start_position[0]
    )
    left = start_position[1] - 1 if start_position[1] > 0 else start_position[1]
    right = (
        end_position[1] + 1
        if end_position[1] < schematic.shape[1] - 1
        else end_position[1]
    )
    for i in range(top, bottom + 1):
        for j in range(left, right + 1):
            if schematic[(i, j)] == GEAR:
                if (i, j) not in gears:
                    gears[(i, j)] = []
                gears[(i, j)].append(number)
    return gears


if __name__ == "__main__":
    # with open("./day03/example_input", "r") as file:
    with open("./day03/input", "r") as file:
        schematic = file.readlines()
    schematic = np.array([[*row.strip()] for row in schematic])
    position = (0, 0)
    gears = {}
    while position:
        number, start_position, end_position = find_next_number(schematic, position)
        if not number:
            break
        gears = find_adjacent_gears(
            start_position, end_position, schematic, gears, number
        )
        position = next_position(end_position, schematic.shape)
    gear_ratios = []
    for numbers in gears.values():
        if len(numbers) == 2:
            gear_ratios.append(numbers[0] * numbers[1])
    print(f"The sum of all of the gear ratios is {sum(gear_ratios)}")
