import sys
import numpy as np
import matplotlib.pyplot as plt

from typing import List

# read file with given filename and get points
def read_file(filename: str) -> np.ndarray:
    points = []

    with open(filename, "r") as file:
        for line in file.readlines():
            point = [float(i) for i in line.rstrip().split(",")]
            points.append(point)

    return np.array(points)


def main() -> None:
    argv, argc = sys.argv, len(sys.argv)
    if (argc != 2):
        usage(argv)
    
    input_file = argv[1]
    # Get points from file
    points = read_file(input_file)
    
    # Create Scatter Plor
    plt.scatter(points[:, 1], points[:, 0], c="orange")
    plt.title("Randomly Generated Points")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig("generated_points_plot.pdf")
    plt.show()
    plt.close()


# Usage error function
def usage(argv: List[str]) -> None:
    print(f"[!] Usage: {argv[0]} <input file>")
    print(f"[!] Example Usage: {argv[0]} input.csv")
    sys.exit()


if __name__ == '__main__':
    main()
