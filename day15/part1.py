import pandas as pd

MULTIPLIER = 17
DIVISOR = 256


def calculate_hash(col: pd.Series) -> int:
    step = [*col.iloc[0]]
    current_value = 0
    for char in step:
        current_value += ord(char)
        current_value *= MULTIPLIER
        current_value %= DIVISOR
    return current_value


if __name__ == "__main__":
    input_df = pd.read_csv("./day15/input", header=None)
    # input_df = pd.read_csv('./day15/example_input',header=None)
    hashes = input_df.apply(calculate_hash)
    print(f"The sum of the results is {sum(hashes)}")
