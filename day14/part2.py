import pandas as pd
from tqdm import tqdm

ROUNDED_ROCK = "O"
CUBE_SHAPED_ROCK = "#"
EMPTY_SPACE = "."

NO_EMPTY_SPACE = -1

CYCLE = {
    "NORTH": {"axis": 0, "reversed": False},
    "WEST": {"axis": 1, "reversed": False},
    "SOUTH": {"axis": 0, "reversed": True},
    "EAST": {"axis": 1, "reversed": True},
}

TOTAL_CYCLES = 1000000000


def tilt_platform(serie, reversed, direction):
    key = (direction, "".join(serie))
    if key in step_memory:
        return pd.Series([*step_memory[key]])
    start = 0
    stop = serie.shape[0]
    step = 1
    if reversed:
        start = serie.shape[0] - 1
        stop = -1
        step = -1
    first_empty_space = NO_EMPTY_SPACE
    for i in range(start, stop, step):
        if serie.iloc[i] == EMPTY_SPACE and first_empty_space == NO_EMPTY_SPACE:
            first_empty_space = i
        elif serie.iloc[i] == ROUNDED_ROCK and first_empty_space != NO_EMPTY_SPACE:
            serie.iloc[i] = EMPTY_SPACE
            serie.iloc[first_empty_space] = ROUNDED_ROCK
            first_empty_space += step
        elif serie.iloc[i] == CUBE_SHAPED_ROCK:
            first_empty_space = NO_EMPTY_SPACE
    step_memory[key] = "".join(serie)
    return serie


def calculate_load(column):
    load = 0
    for i in range(column.shape[0]):
        if column.iloc[i] == ROUNDED_ROCK:
            load += column.shape[0] - i
    return load


def flatten_df(df):
    return "".join(df.values.flatten())


def reshape_df(flat_df, df_shape):
    rows = []
    for i in range(0, df_shape[0] * df_shape[1], df_shape[1]):
        row = list(flat_df[i : i + df_shape[1]])
        rows.append(row)
    df = pd.DataFrame(rows)
    return df


if __name__ == "__main__":
    step_memory = {}
    # cycle_memory = {}
    state_history = {}
    platform_df = pd.read_fwf("./day14/input", widths=[1] * 100, header=None)
    # platform_df = pd.read_fwf("./day14/example_input", widths=[1] * 10, header=None)
    for iteration in tqdm(range(TOTAL_CYCLES)):
        key = flatten_df(platform_df)
        # if key in cycle_memory:
        #     platform_df = reshape_df(cycle_memory[key], platform_df.shape)
        #     continue
        if key in state_history:
            pattern_start = state_history[key]
            pattern_length = iteration - pattern_start
            break
        state_history[key] = iteration
        for direction, tilt in CYCLE.items():
            platform_df = platform_df.apply(
                tilt_platform, axis=tilt["axis"], args=(tilt["reversed"], direction)
            )
        # cycle_memory[key] = flatten_df(platform_df)
    if pattern_length:
        remaining_iterations = (TOTAL_CYCLES - pattern_start) % pattern_length
        platform_df = reshape_df(key, platform_df.shape)
        for _ in range(remaining_iterations):
            for direction, tilt in CYCLE.items():
                platform_df = platform_df.apply(
                    tilt_platform, axis=tilt["axis"], args=(tilt["reversed"], direction)
                )
    loads = platform_df.apply(calculate_load)
    print(f"Total load on the north support beams: {sum(loads)}")
