import sys
from itertools import combinations
import math
from a1_utils import read_input_from_cli, distance, write_output_to_file, sort_pairs

def brute_force_closest_pair(points: list[tuple[float, float]]) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
    """
    Find the closest pair of points using brute force.
    
    Args:
        points (list[tuple[float, float]]): A list of 2D points, where each point is represented 
                                            as a tuple of coordinates (x, y).
                                            
    Returns:
        tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
            - The updated minimum distance (float) between the closest pair(s) of points.
            - A list of tuples representing the closest point pairs, where each pair is a 
              tuple of two points ((x1, y1), (x2, y2)).
    """
    min_dist = float('inf')
    closest_pairs = []
    
    for p1, p2 in combinations(points, 2):
        dist = distance(p1, p2)
        if dist < min_dist:
            min_dist = dist
            closest_pairs = [(p1, p2)] #update the closest pair
        elif dist == min_dist:
            closest_pairs.append((p1,p2))
    return min_dist, closest_pairs

def split_points_to_two_parts(points_sorted_by_x):
    """
    Split points into two parts.
    
    Args:
        points (list[tuple[float, float]]): A list of 2D points where 
                                            each point is represented as a tuple (x, y).
                                            This list must sorted by x.
    Returns:
        median_x: the value of median x
        points_l: The left part points
        points_r: The right part points
    """

    n = len(points_sorted_by_x)
    i_split = n // 2 if n % 2 == 1 else n // 2 - 1
    median_x = points_sorted_by_x[i_split][0]
    points_l = points_sorted_by_x[0:i_split]
    points_r = points_sorted_by_x[i_split:]
    return median_x, points_l, points_r

def closest_cross_pair(My, delta):
    """
    Find the closest pair of points across the division line.
    
    Args:
        My (list of tuple): List of points sorted by y-coordinate that are within delta from the division line L.
        delta (float): The minimum distance found from the left and right halves.
    
    Returns:
        min_dist: The minimum distance found across the division line.
        closest_pairs: A list of point pairs that are the closest pairs.
    """
    min_dist = float('inf') 
    closest_pairs = []
    
    # Iterate over each point in the sorted list My
    for i in range(len(My)):
        for j in range(i + 1, len(My)):
            # Stop if the y-distance between the points is greater than delta
            # The maximum comparison time is 7
            if My[j][1] - My[i][1] > delta:
                break
            # Calculate the distance between My[i] and My[j]
            dist = distance(My[i], My[j])
            
            # If we find a smaller distance than delta, update the distance and pairs
            if dist < min_dist:
                min_dist = dist
                closest_pairs = [(My[i], My[j])]
            # If the distance equals the current minimum, add this pair to the closest_pairs list
            elif dist == min_dist:
                closest_pairs.append((My[i], My[j]))
    return min_dist, closest_pairs

def merge_closest_pairs(delta_l, points_min_l, delta_r, points_min_r, delta_cross, points_min_cross):
    """
    Compare three delta values and return the smallest delta with corresponding point pairs.
    If there are equal delta values, merge the point pairs.

    Args:
        delta_l (float): Minimum distance for the left half.
        points_min_l (list): List of point pairs with the minimum distance in the left half.
        delta_r (float): Minimum distance for the right half.
        points_min_r (list): List of point pairs with the minimum distance in the right half.
        delta_cross (float): Minimum distance for the cross pairs.
        points_min_cross (list): List of point pairs with the minimum distance across the division line.

    Returns:
        min_delta: The smallest delta.
        closest_pairs: The list of point pairs corresponding to the smallest delta.
    """
    # Find the smallest delta value
    min_delta = min(delta_l, delta_r, delta_cross)
    
    # Initialize closest pairs list
    closest_pairs = []
    
    # Check if delta_l is equal to the minimum delta
    if min_delta == delta_l:
        closest_pairs.extend(points_min_l)
    
    # Check if delta_r is equal to the minimum delta
    if min_delta == delta_r:
        closest_pairs.extend(points_min_r)
    
    # Check if delta_cross is equal to the minimum delta
    if min_delta == delta_cross:
        closest_pairs.extend(points_min_cross)

    # Remove duplicate pairs (doesn't ignore order, because we dont want to sort anything in a recurisive function)
    closest_pairs = list(set([tuple(map(tuple, pair)) for pair in closest_pairs]))
    return min_delta, closest_pairs

def recurisive_enhanced_divide_and_conquer_closest_pair(points_sorted_by_x, points_sorted_by_y):
    """
    Recursively find the closest pair of points using a divide-and-conquer approach.
    
    Args:
        points_sorted_by_x: A list of 2D points which sorted by x.
        points_sorted_by_y: A list of 2D points which sorted by y.
                                            
    Returns:
        min_delta: The minimum distance between the closest pair(s) of points.
        closest_pairs: A list of closest point pairs.
    """
    if len(points_sorted_by_x) <= 3:
        return brute_force_closest_pair(points_sorted_by_x)
    else:
        median_x, points_l_sorted_by_x, points_r_sorted_by_x = split_points_to_two_parts(points_sorted_by_x)

        points_l_sorted_by_y = [point for point in points_sorted_by_y if point in points_l_sorted_by_x]
        points_r_sorted_by_y = [point for point in points_sorted_by_y if point in points_r_sorted_by_x]

        delta_l, points_min_l = recurisive_enhanced_divide_and_conquer_closest_pair(points_l_sorted_by_x, points_l_sorted_by_y)
        delta_r, points_min_r = recurisive_enhanced_divide_and_conquer_closest_pair(points_r_sorted_by_x, points_r_sorted_by_y)
        delta_min = min(delta_l, delta_r)

        points_cross = [point for point in points_sorted_by_y if abs(point[0] - median_x) <= delta_min]

        delta_cross, points_min_cross = closest_cross_pair(points_cross, delta_min)
        min_delta, closest_pairs = merge_closest_pairs(delta_l, points_min_l, delta_r, points_min_r, delta_cross, points_min_cross)
        return min_delta, closest_pairs

def enhanced_divide_and_conquer_closest_pair(points: list[tuple[float, float]]) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
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
    
    # TODO 
    # Pre-sort all points based on 𝑥 and 𝑦 coordinates respectively
    points_sorted_by_x = sorted(points, key=lambda point: point[0])
    points_sorted_by_y = sorted(points, key=lambda point: point[1])
    min_delta, closest_pairs =  recurisive_enhanced_divide_and_conquer_closest_pair(points_sorted_by_x, points_sorted_by_y)
    # Remove duplicate pairs (ignoring order) from 'closest_pairs'
    closest_pairs = list(set([tuple(sorted(map(tuple, pair))) for pair in closest_pairs]))
    return min_delta, closest_pairs

if __name__ == "__main__":
    try:
        points = read_input_from_cli()
        min_dist, closest_pairs = enhanced_divide_and_conquer_closest_pair(points)
        closest_pairs = sort_pairs(closest_pairs)
        print(f"Minimum Distance: {min_dist}")
        print("Closest Pairs:")
        for pair in closest_pairs:
            print(pair)
        write_output_to_file(distance=min_dist, points=closest_pairs, output_file= 'enhance_ddnc_output.txt')
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
