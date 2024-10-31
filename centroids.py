# centroids.py

import numpy as np
import time
from sklearn.neighbors import KDTree
import config

# Config data
max_distance = config.max_distance

def agglomerative_centroid_clustering(points):
    num_points = len(points)
    clusters = {i: [i] for i in range(num_points)}  # Index to list of point indices in the cluster,        f.e. clusters = {2: [2], 5: [5], 7: [7]}
    centroids = {i: points[i].astype(float) for i in range(num_points)}  # Index to centroid coordinates,   f.e. centroids = {2: [1.0, 2.0], 5: [3.0, 4.0], 7: [5.0, 6.0]}
    active_clusters = list(clusters.keys())  # List of active cluster indices,                              f.e. active_clusters = [2, 5, 7]

    print("Сentroid сlusterization...")

    iteration = 0
    total_start_time = time.time()

    while len(active_clusters) > 1:
        iteration += 1

        # Getting centroid coordinates of current clusters
        centroid_coords = np.array([centroids[i] for i in active_clusters])                                 # f.e. centroid_coords = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
        index_to_id = {idx: cluster_id for idx, cluster_id in enumerate(active_clusters)}                   # f.e. index_to_id = {0: 2, 1: 5, 2: 7 }

        # Build k-d tree on centroids
        tree = KDTree(centroid_coords)

        # Set k greater than 2 to have a buffer of neighbors in case of ties                                # f.e. if k = 2,
        k = min(10, len(active_clusters))                                                                   # f.e. distances = [[0.0, 2.83], [0.0, 2.83], [0.0, 2.83]]
        distances, indices = tree.query(centroid_coords, k=k)                                               # f.e. indices = [[0, 1],[1, 0],[2, 1]]

        min_distance = np.inf
        min_pair = None

        for idx, (dist_list, ind_list) in enumerate(zip(distances, indices)):
            i = index_to_id[idx]
            # Find the nearest cluster that is not itself
            for dist, neighbor_idx in zip(dist_list[1:], ind_list[1:]):  # Start from [1:] to skip itself
                if neighbor_idx != idx:
                    j = index_to_id[neighbor_idx]
                    break
            else:
                # If none found, skip this cluster
                continue

            # Check if the current pair has the minimum distance
            if dist < min_distance:
                min_distance = dist
                min_pair = (i, j)

        if min_pair is None:
            print(f"\rIteration {iteration}, No valid pairs found", end="")
            break

        if min_distance > max_distance:
            print(f"\rIteration {iteration}, Min Distance ({min_distance:.2f}) > Max Distance ({max_distance})", end="")
            break

        i, j = min_pair

        iteration_time = time.time() - total_start_time
        print(f"\rIteration {iteration}, Unified clusters {i} and {j}, Distance {min_distance:.2f}, Time: {iteration_time:.2f}s",end="")

        # Merge clusters i and j
        clusters[i].extend(clusters[j])
        active_clusters.remove(j)
        del clusters[j]
        del centroids[j]

        # Update centroid of the merged cluster
        centroids[i] = np.mean(points[clusters[i]], axis=0)

    print("\nDone")

    total_time = time.time() - total_start_time
    print(f"Total time {total_time:.2f}s, Iterations {iteration}")

    return clusters, centroids