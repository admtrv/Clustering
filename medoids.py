# medoids.py

import numpy as np
import time
from sklearn.neighbors import KDTree
import config

# Config data
max_distance = config.max_distance

def agglomerative_medoid_clustering(points):
    num_points = len(points)
    clusters = {i: [i] for i in range(num_points)}
    medoids = {i: points[i].astype(float) for i in range(num_points)}
    active_clusters = list(clusters.keys())

    print("Medoid clusterization...")

    iteration = 0
    total_start_time = time.time()

    while len(active_clusters) > 1:
        iteration += 1

        medoid_coords = np.array([medoids[i] for i in active_clusters])
        index_to_id = {idx: cluster_id for idx, cluster_id in enumerate(active_clusters)}

        tree = KDTree(medoid_coords)

        k = min(10, len(active_clusters))
        distances, indices = tree.query(medoid_coords, k=k)

        min_distance = np.inf
        min_pair = None

        for idx, (dist_list, ind_list) in enumerate(zip(distances, indices)):
            i = index_to_id[idx]
            for dist, neighbor_idx in zip(dist_list[1:], ind_list[1:]):
                if neighbor_idx != idx:
                    j = index_to_id[neighbor_idx]
                    break
            else:
                continue

            if dist < min_distance:
                min_distance = dist
                min_pair = (i, j)

        if min_pair is None:
            print(f"\rIteration {iteration}, No valid pairs", end="")
            break

        if min_distance > max_distance:
            print(f"\rIteration {iteration}, Min Distance ({min_distance:.2f}) > Max Distance ({max_distance})", end="")
            break

        i, j = min_pair

        iteration_time = time.time() - total_start_time
        print(f"\rIteration {iteration}, Unified clusters {i} and {j}, Distance {min_distance:.2f}, Time: {iteration_time:.2f}s", end="")

        clusters[i].extend(clusters[j])
        active_clusters.remove(j)
        del clusters[j]
        del medoids[j]

        cluster_point_indices = clusters[i]
        cluster_points = points[cluster_point_indices]

        distances_matrix = np.linalg.norm(cluster_points[:, np.newaxis] - cluster_points[np.newaxis, :], axis=2)
        sum_distances = np.sum(distances_matrix, axis=1)
        min_index = np.argmin(sum_distances)
        medoids[i] = cluster_points[min_index]

    print("\nDone")

    total_time = time.time() - total_start_time
    print(f"Total time {total_time:.2f}s, Iterations {iteration}")

    return clusters, medoids