import pandas as pd

NUMBER_STRINGS_MAP = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}


def get_calibration_value(row: pd.Series) -> int:
    line = row.iloc[0]
    first_digit = -1
    first_digit_pos = len(line)
    last_digit = -1
    last_digit_pos = -1
    for substring in NUMBER_STRINGS_MAP.keys():
        pos = line.find(substring)
        if first_digit_pos != 0 and pos != -1 and pos < first_digit_pos:
            first_digit_pos = pos
            first_digit = NUMBER_STRINGS_MAP[substring]
        pos = line.rfind(substring)
        if last_digit_pos != len(line) - 1 and pos > last_digit_pos:
            last_digit_pos = pos
            last_digit = NUMBER_STRINGS_MAP[substring]
    return int(f"{first_digit}{last_digit}")


if __name__ == "__main__":
    # input_df = pd.read_csv("./day01/example_input", header=None)
    input_df = pd.read_csv("./day01/input", header=None)
    calibration_values = input_df.apply(get_calibration_value, axis=1)
    print(f"The sum of all of the calibration values is {sum(calibration_values)}")
