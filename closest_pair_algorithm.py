import sys
import time
import math
from typing import List, Tuple


def read_file(filename: str) -> List[Tuple[float, float]]:
    points = []

    with open(filename, "r") as file:
        for line in file.readlines():
            point = [float(i) for i in line.rstrip().split(",")]
            points.append(point)

    return points


def get_distance(p1: Tuple[float, float], p2: Tuple[float, float]):
    return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))


def bf_CPA(points: List[Tuple]) -> float:
    N = len(points)
    if N == 2:
        return get_distance(points[0], points[1])
    
    min_distance = math.inf
    for i in range(N - 1):
        for j in range(i + 1, N):
            min_distance = min(min_distance, get_distance(points[i], points[j]))
    return min_distance


def get_strip_points(points, N, mean, min_distance):
    S = [] # Strip
    M = 0 # size of strip

    for point in points:
        # Check if point is in strip
        if mean - min_distance < point[1] < mean + min_distance:
            # point is in strip
            S.append(point)
            M += 1

    return S, M


def merge(left, right):
    if not len(left) or not len(right):
        return left or right
 
    result = []
    i, j = 0, 0
    while (len(result) < len(left) + len(right)):
        if left[i][0] < right[j][0]:
            result.append(left[i])
            i+= 1
        else:
            result.append(right[j])
            j+= 1
        if i == len(left) or j == len(right):
            result.extend(left[i:] or right[j:])
            break
 
    return result


def optimized_CPA(points: List[tuple]) -> float:
    # Sort list according to x-axis
    points.sort(key=lambda point : point[1])

    def solve(points, N):
        if N == 2:
            return get_distance(points[0], points[1]), sorted(points, key=lambda point : point[0])
        
        mid = N // 2
        d_1, y_L = solve(points[:mid], mid)
        d_2, y_R = solve(points[mid:], mid)
        min_distance = min(d_1, d_2)

        # Used to get the centre divide - average x value between
        # the last point in points_L and the first point in points_R
        mean = (points[mid - 1][1] + points[mid][1]) / 2
        y = merge(y_L, y_R)
        
        S, M = get_strip_points(y, N, mean, min_distance)

        # Get the min distance in the strip
        for i in range(M - 1):
            j = 1
            # Only consider the first 7
            while i + j < M and j <= 7:
                min_distance = min(min_distance, get_distance(S[i], S[i + j]))
                j += 1

        return min_distance, y

    return solve(points, len(points))[0]


def main():
    argv, argc = sys.argv, len(sys.argv)
    if (argc != 2):
        usage(argv)
    
    points = read_file(argv[1])
    print(len(points))

    start = time.time()
    distance = bf_CPA(points)
    end = time.time()
    print(f"Distance: {distance:.4f} Time: {(end - start) * 1_000:.2f}ms")

    start = time.time()
    distance = optimized_CPA(points)
    end = time.time()
    print(f"Distance: {distance:.4f} Time: {(end - start) * 1_000:.2f}ms")


def usage(argv):
    print(f"[!] Usage: {argv[0]} <input file>")
    print(f"[!] Example Usage: {argv[0]} input.txt")
    sys.exit()


if __name__ == "__main__":
    main()
