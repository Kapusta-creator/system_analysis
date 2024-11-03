import json
import math


def task(json_str: str):
    extensional_lengths = json.loads(json_str)
    h = 0.0
    for i in range(len(extensional_lengths)):
        for j in range(len(extensional_lengths[i])):
            if extensional_lengths[i][j] != 0:
                h += extensional_lengths[i][j] / (len(extensional_lengths) - 1) * \
                     math.log2(extensional_lengths[i][j] / (len(extensional_lengths) - 1))
    return round(-h, 1)


if __name__ == "__main__":
    example_str = """[
        [2, 0, 2, 0, 0],
        [0, 1, 0, 0, 1],
        [2, 1, 0, 0, 1],
        [0, 1, 0, 1, 1],
        [0, 1, 0, 1, 1]
    ]"""
    print(task(example_str))


