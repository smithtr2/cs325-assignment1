# cs325-assignment1

Pseudocode of brute＿force

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
