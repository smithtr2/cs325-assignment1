"""
Name: divide_conquer.py
Author: Trevor Smith
Email: smithtr2@oregonstate.edu
Github: smithtr2
"""

import sys
from itertools import combinations
import math
from a1_utils import read_input_from_cli, distance, write_output_to_file, sort_pairs

def divide_and_conquer_closest_pair(points: list[tuple[float, float]]) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
    """
    Recursively find the closest pair of points using a divide-and-conquer approach.
    
    Args:
        points (list[tuple[float, float]]): A list of 2D points where 
                                            each point is represented as a tuple (x, y).
                                            
    Returns:
        tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
            - The minimum distance between the closest pair(s) of points.
            - A list of tuples representing the closest point pairs, where each pair is a 
              tuple of two points ((x1, y1), (x2, y2)).
    """

    #sort points by x-coordinate to start, sort by y-coordinate later each time in recursive function
    points.sort(key=lambda p: p[0])

    def closest_pair_recursive(pts):
        n = len(pts)

        #base case
        if n <= 3:
            min_dist = float('inf')
            pairs = []
            for p1, p2 in combinations(pts, 2):
                d = distance(p1, p2)
                if d < min_dist:
                    min_dist = d
                    pairs = [(p1, p2)]
                elif d == min_dist:
                    pairs.append((p1, p2))
            return min_dist, sort_pairs(pairs)

        #split the currect list of points into two halves
        middle = n // 2 #handy division with no remainder
        left = pts[:middle]
        right = pts[middle:]

        #run recursion on both halves
        d1, pairs1 = closest_pair_recursive(left)
        d2, pairs2 = closest_pair_recursive(right)

        #combine the two halves together
        d = min(d1, d2)
        pairs = []
        if d == d1:
            pairs.extend(pairs1)
        if d == d2:
            pairs.extend(pairs2)

        #set search to only search the strip
        xmiddle = pts[middle][0]
        strip = [p for p in pts if abs(p[0] - xmiddle) < d] #list only containing points in x strip.
        strip.sort(key=lambda p: p[1]) #here is the y-coordinate search every recursive

        #search each pair in the strip, could be o(n^2) if all points are in strip for asymptotic runtime.
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if strip[j][1] - strip[i][1] >= d:
                    break
                dstrip = distance(strip[i], strip[j])
                if dstrip < d:
                    d = dstrip
                    pairs = [(strip[i], strip[j])]
                elif dstrip == d:
                    if (strip[i], strip[j]) not in pairs and (strip[j], strip[i]) not in pairs:
                        pairs.append((strip[i], strip[j]))


        #sort pairs and return
        pairs = sort_pairs(pairs)
        return d, pairs

    return closest_pair_recursive(points)


if __name__ == "__main__":
    try:
        points = read_input_from_cli()
        min_dist, closest_pairs = divide_and_conquer_closest_pair(points)

        print(f"Minimum Distance: {min_dist}")
        print("Closest Pairs:")
        for pair in closest_pairs:
            print(pair)
        write_output_to_file(distance=min_dist, points=closest_pairs, output_file= 'ddnc_output.txt')
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)