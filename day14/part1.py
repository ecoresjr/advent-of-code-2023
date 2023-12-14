import pandas as pd


ROUNDED_ROCK = "O"
CUBE_SHAPED_ROCK = "#"
EMPTY_SPACE = "."

NO_EMPTY_SPACE = -1


def tilt_north_and_calculate_load(column):
    load = 0
    first_empty_space = -1
    for i in range(column.shape[0]):
        if column.iloc[i] == EMPTY_SPACE and first_empty_space == NO_EMPTY_SPACE:
            first_empty_space = i
        elif column.iloc[i] == ROUNDED_ROCK and first_empty_space != NO_EMPTY_SPACE:
            column.iloc[i] = EMPTY_SPACE
            column.iloc[first_empty_space] = ROUNDED_ROCK
            load += column.shape[0] - first_empty_space
            first_empty_space += 1
        elif column.iloc[i] == ROUNDED_ROCK and first_empty_space == NO_EMPTY_SPACE:
            load += column.shape[0] - i
        elif column.iloc[i] == CUBE_SHAPED_ROCK:
            first_empty_space = NO_EMPTY_SPACE
    return load


if __name__ == "__main__":
    input_df = pd.read_fwf("./day14/input", widths=[1] * 100, header=None)
    loads = input_df.apply(tilt_north_and_calculate_load)
    print(f"Total load on the north support beams: {sum(loads)}")
