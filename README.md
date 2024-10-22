## Agglomerative Centroid Clustering

### Initialization

- `num_points = len(points)`: Determines the number of points for clustering.
- `clusters = {i: [i] for i in range(num_points)}`: Initializes a dictionary where each point starts as a separate cluster.
- `centroids = {i: points[i].astype(float) for i in range(num_points)}`: Initializes a dictionary where the initial centroid for each cluster is the point itself.

### Distance Matrix Initialization

- `distance_matrix = np.full((num_points, num_points), np.inf)`: Initializes a square matrix filled with infinity values to store distances between pairs of points.
- For each pair of points `(i, j)`, the Euclidean distance is calculated and stored in `distance_matrix[i, j]`.

### Main Clustering Loop

- The algorithm continues merging clusters until only one active cluster remains or the stopping condition is met.
- In each iteration:
  - The closest pair of clusters `(i, j)` with the minimum distance `min_distance` is found.
  - If the distance `min_distance` exceeds `max_average_distance`, the algorithm terminates.
  - Otherwise, clusters `i` and `j` are merged:
    - The points from cluster `j` are added to cluster `i`, and cluster `j` is removed.
    - `active_clusters.remove(j)`: Cluster `j` is removed from the set of active clusters.
    - The centroid of cluster `i` is updated as the average of all the points in the newly merged cluster.

### Updating the Distance Matrix

- After merging clusters `i` and `j`, the distance matrix is updated:
  - For each active cluster `k` connected to `i`, the distance between the updated centroid of cluster `i` and the centroid of cluster `k` is recalculated.
  - The new distance is updated in the matrix for the pairs `(i, k)` and `(k, i)`.

### Algorithm Termination

- The algorithm terminates when all possible clusters are merged.
- Or when the distance between the nearest clusters exceeds `max_average_distance`.
