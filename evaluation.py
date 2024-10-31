# evaluation.py

import numpy as np
import config

# Config data
max_average_distance = config.max_average_distance

def evaluate_clustering(points, clusters, centers):
    total_clusters = len(clusters)
    successful_clusters = 0
    cluster_average_distances = {}

    for cluster_id, point_indices in clusters.items():
        cluster_points = points[point_indices]
        center = centers[cluster_id]
        distances = np.linalg.norm(cluster_points - center, axis=1)
        average_distance = np.mean(distances)
        cluster_average_distances[cluster_id] = average_distance

        if average_distance <= max_average_distance:
            successful_clusters += 1

    success_percentage = (successful_clusters / total_clusters) * 100

    print(f"Success rate {success_percentage:.2f}%")