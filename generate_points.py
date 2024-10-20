import sys
from random import random

MAX_HEIGHT = 100
MAX_WIDTH = 100


def generate_point():
    x = MAX_WIDTH * (random() * 2 - 1)
    y = MAX_HEIGHT * (random() * 2 - 1)
    return x, y


def main():
    argv, argc = sys.argv, len(sys.argv)
    if (argc != 3):
        usage(argv)

    nPoints = int(argv[1])
    output_file = argv[2]

    with open(output_file, "w") as file:
        for _ in range(2 ** nPoints):
            point = generate_point()
            file.write(f"{point[0]},{point[1]}\n")


def usage(argv):
    print(f"[!] Usage: python/python3 {argv[0]} <number of points> <output file>")
    print(f"[!] Example Usage: python/python3 {argv[0]} 10 (2^10 points) output.txt")
    sys.exit()


if __name__ == "__main__":
    main()
