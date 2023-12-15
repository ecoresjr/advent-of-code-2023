import pandas as pd


def get_calibration_value(row: pd.Series) -> int:
    line = [*row.iloc[0]]
    calibration_value = []
    for char in line:
        if char.isdigit():
            calibration_value.append(char)
            break
    for char in reversed(line):
        if char.isdigit():
            calibration_value.append(char)
            break
    return int("".join(calibration_value))


if __name__ == "__main__":
    # input_df = pd.read_csv("./day01/example_input", header=None)
    input_df = pd.read_csv("./day01/input", header=None)
    calibration_values = input_df.apply(get_calibration_value, axis=1)
    print(f"The sum of all of the calibration values is {sum(calibration_values)}")
