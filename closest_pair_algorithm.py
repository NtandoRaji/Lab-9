import sys
import time
import math
from typing import List, Tuple

# Gets points from file with the given filename
def read_file(filename: str) -> List[Tuple[float, float]]:
    points = []

    with open(filename, "r") as file:
        for line in file.readlines():
            point = [float(i) for i in line.rstrip().split(",")]
            points.append(point)

    return points

# Get the euclidean distance between points 
def get_distance(p1: Tuple[float, float], p2: Tuple[float, float]):
    return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))


def bf_CPA(points: List[Tuple]) -> float:
    N = len(points)
    if N == 2:
        # Only have two points, return distance
        return get_distance(points[0], points[1])
    
    # Get min distance between points
    min_distance = math.inf
    for i in range(N - 1):
        for j in range(i + 1, N):
            min_distance = min(min_distance, get_distance(points[i], points[j]))
    
    return min_distance


def get_strip_points(points: List[Tuple], N: int, mean: float, min_distance: float) -> Tuple[List[Tuple], int]:
    S = [] # Strip
    M = 0 # size of strip

    for point in points:
        # Check if point is in strip
        if mean - min_distance < point[1] < mean + min_distance:
            # point is in strip
            S.append(point)
            M += 1

    return S, M


def merge(y_left: List[Tuple[int, int]], y_right: List[Tuple[int, int]]):
    if not len(y_left) or not len(y_right):
        return y_left or y_right
 
    y = []
    i, j = 0, 0
    while (len(y) < len(y_left) + len(y_right)):
        
        if y_left[i][0] < y_right[j][0]:
            y.append(y_left[i])
            i += 1

        else:
            y.append(y_right[j])
            j += 1

        if i == len(y_left) or j == len(y_right):
            y.extend(y_left[i:] or y_right[j:])
            break
 
    return y


def optimized_CPA(points: List[Tuple[int, int]]) -> float:
    # Preprocessing: Sort points according to x values
    points.sort(key=lambda point : point[1])

    def solve(points: List[Tuple[int, int]], N: int):
        # check if there are only two points
        if N == 2:
            # return distance between points & the points sortes according to y values
            return get_distance(points[0], points[1]), sorted(points, key=lambda point : point[0])
        
        mid = N // 2 # split points into subsets
        d_1, y_left = solve(points[:mid], mid) # get min distance & sorted y from left subset
        d_2, y_right = solve(points[mid:], mid) # get min distance & sorted y from right subset
        min_distance = min(d_1, d_2)

        # Used to get the centre divide - average x value between
        # the last point in points_L and the first point in points_R
        mean = (points[mid - 1][1] + points[mid][1]) / 2
        y = merge(y_left, y_right)
        
        # Get points in strip and size of strip
        S, M = get_strip_points(y, N, mean, min_distance)

        # Get the min distance in the strip
        for i in range(M - 1):
            j = 1
            # Only consider the first 5 points closest to the current point (better than 7)
            while i + j < M and j <= 5:
                min_distance = min(min_distance, get_distance(S[i], S[i + j]))
                j += 1

        return min_distance, y

    # Only return the min distance
    return solve(points, len(points))[0]


def main():
    argv, argc = sys.argv, len(sys.argv)
    if (argc != 2):
        usage(argv)
    
    # Read file to get points
    points = read_file(argv[1])

    # Run and time brute force implementation
    start = time.time()
    distance = bf_CPA(points)
    end = time.time()
    print(f"Distance: {distance:.4f} Time: {(end - start) * 1_000:.2f}ms")

    # Run and time optimized implementation
    start = time.time()
    distance = optimized_CPA(points)
    end = time.time()
    print(f"Distance: {distance:.4f} Time: {(end - start) * 1_000:.2f}ms")


# Usage error function
def usage(argv):
    print(f"[!] Usage: {argv[0]} <input file>")
    print(f"[!] Example Usage: {argv[0]} input.csv")
    sys.exit()


if __name__ == "__main__":
    main()
