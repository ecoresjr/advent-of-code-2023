from typing import Tuple

import pandas as pd

MULTIPLIER = 17
DIVISOR = N_BOXES = 256

REMOVE = "-"
ADD_REPLACE = "="


def calculate_hash(label: str) -> int:
    current_value = 0
    for char in [*label]:
        current_value += ord(char)
        current_value *= MULTIPLIER
        current_value %= DIVISOR
    return current_value


def encode_steps(col: pd.Series) -> Tuple[int, str, str, int | None]:
    step = col.iloc[0]
    if REMOVE in step:
        op = REMOVE
    else:
        op = ADD_REPLACE
    label, lens = step.split(op)
    box = calculate_hash(label)
    return (box, label, op, int(lens) if lens else None)


if __name__ == "__main__":
    input_df = pd.read_csv("./day15/input", header=None)
    # input_df = pd.read_csv("./day15/example_input", header=None)
    steps_df = input_df.apply(encode_steps)
    steps_df = steps_df.T

    boxes = {i: {} for i in range(N_BOXES)}
    for _, step in steps_df.iterrows():
        box, label, op, lens = step.values
        if op == REMOVE and label in boxes[box]:
            del boxes[box][label]
        elif op == ADD_REPLACE:
            boxes[box][label] = lens

    total_focusing_power = 0
    for box, lenses in boxes.items():
        box_focusing_power = 0
        lenses = list(lenses.values())
        for i in range(len(lenses)):
            box_focusing_power += (box + 1) * (i + 1) * lenses[i]
        total_focusing_power += box_focusing_power

    print(
        f"The focusing power of the resulting lens configuration is {total_focusing_power}"
    )
