import pandas as pd

if __name__ == "__main__":
    # with open("./day02/example_input", "r") as file:
    with open("./day02/input", "r") as file:
        lines = file.readlines()
    game_powers = []
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
        df = df.max()
        power = 1
        for n in df.values:
            power *= n
        game_powers.append(power)
    print(
        f"The sum of the power of all minimum sets of cubes is {int(sum(game_powers))}"
    )
