import pandas as pd

RED_CUBES = 12
GREEN_CUBES = 13
BLUE_CUBES = 14


def is_game_possible(row: pd.Series) -> bool:
    return (
        (not pd.notna(row["green"]) or row["green"] <= GREEN_CUBES)
        and (not pd.notna(row["blue"]) or row["blue"] <= BLUE_CUBES)
        and (not pd.notna(row["red"]) or row["red"] <= RED_CUBES)
    )


if __name__ == "__main__":
    # with open("./day02/example_input", "r") as file:
    with open("./day02/input", "r") as file:
        lines = file.readlines()
    possible_game_ids = []
    for line in lines:
        id, line = line.strip().replace("Game ", "").split(":")
        line = line.strip().split(";")
        line = [part.split(",") for part in line]
        data = []
        for part in line:
            part_dict = {}
            for subpart in part:
                part_dict[subpart.strip().split(" ")[1]] = int(
                    subpart.strip().split(" ")[0]
                )
            data.append(part_dict)
        df = pd.DataFrame(data)
        df = df.apply(is_game_possible, axis=1)
        if df.all():
            possible_game_ids.append(int(id))
    print(
        f"The sum of the IDs of games that would have been posible is {sum(possible_game_ids)}"
    )
