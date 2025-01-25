# cs325-assignment1

## Pseudocode of brute＿force

Function brute_force_closest_pair (points)
	Initialize min_dist = infinity
	Initialized closest_pairs = [ ]
	For each pair of points (p1, p2) in the set of points:
		Compute the dist between p1 and p2
		If dist < min_dist :
		  Update min_dist = dist
			Reset closest_pairs to [(p1,p2)]
		Else if dist == min_dist:
			Append (p1,p2) to closest_pairs
	Sort each pair of points in closest_pairs
  Sort the entire closest_pairs list by the coordinates of x and y
	Return min_dist and closest_pairs

Main program:
Try:
  Read the input point set points from the command line
  Call brute_force_closest_pair(points) to compute:
    min_dist (minimum distance between points)
    closest_pairs (list of closest point pairs)
  Output:
    min_dist (minimum distance)
    closest_pairs (the closest point pairs)
    Write the results to the file 'brute_force_output.txt'
If an error occurs:
  Output an error message
  Exit the program

## Pseudocode of enhanced divide and conquer
```
Function split_points_to_two_parts(sorted_points_by_x):
    # Split the list of points based on the x-coordinate.
    find the middle index of the points list
    median_x = the x value of the middle point
    points_l = the left part points
    points_r = the right part points
    return median_x, points_l, points_r

Function closest_cross_pair(My, delta):
    # Find the closest pair of points across the division line.
    # My is a list of points sorted by y-coordinate that are within delta from the division line L.
    # delta is the minimum distance found from the left and right halves.
    Initialize min_dist = infinity
    Initialize closest_pairs = []

    for i in range(length of My):
        for j in range(i + 1, len(My)):
            Stop if the y-distance between the points is greater than delta, the maximum comparison time is 7.
            Calculate the distance between My[i] and My[j]
            dist = distance(My[i], My[j])
            if dist < min_dist:
                Update the distance min_dist = dist
                Update the closest_pairs = [(My[i], My[j])]
            elif dist == min_dist:
                add this pair (My[i], My[j]) to the closest_pairs list
    return min_dist, closest_pairs

Function merge_closest_pairs(delta_l, points_min_l, delta_r, points_min_r, delta_cross, points_min_cross):
    # Compare the three deltas and return the smallest one along with corresponding pairs.
    Initialize closest_pairs = []
    Set min_delta to the smallest value among delta_l, delta_r, delta_cross
    if delta_l == min_delta:
        add points_min_l into closest_pairs
    if delta_r == min_delta:
        add points_min_r into closest_pairs
    if delta_cross == min_delta:
        add points_min_cross into closest_pairs
    Remove duplicate pairs (doesn't ignore order, because we dont want to sort anything in a recurisive function) from closest_pairs
    return min_delta, closest_pairs

Function recursive_enhanced_divide_and_conquer_closest_pair(points_sorted_by_x, points_sorted_by_y):
    # Recursively find the closest pair of points using the divide-and-conquer approach.
    if len(points_sorted_by_x) <= 3:
        brute force closest pairs
    else:
        median_x, points_l_sorted_by_x, points_r_sorted_by_x = split_points_to_two_parts(points_sorted_by_x)
        # use the sorted points list to simplify the sorting process
        points_l_sorted_by_y = [point for point in points_sorted_by_y if point in points_l_sorted_by_x]
        points_r_sorted_by_y = [point for point in points_sorted_by_y if point in points_r_sorted_by_x]

        delta_l, points_min_l = recurisive_enhanced_divide_and_conquer_closest_pair(points_l_sorted_by_x, points_l_sorted_by_y)
        delta_r, points_min_r = recurisive_enhanced_divide_and_conquer_closest_pair(points_r_sorted_by_x, points_r_sorted_by_y)
        delta_min = min(delta_l, delta_r)

        Find the closest pairs(points_cross) accross the division line 
        Merge the results (left, right, cross) and return the minimum distance and pairs.

Function enhanced_divide_and_conquer_closest_pair(points):
    # Main function to find the closest pair of points.
    Pre-sort all points based on x and y coordinates respectively
    Call the recursive function recursive_enhanced_divide_and_conquer_closest_pair to find the min_delta and closest_pairs.
    Sort closest_pairs
    return the final minimum distance and the closest pairs.
```