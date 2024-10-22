# visualization.py

import os
import numpy as np
from matplotlib import pyplot as plt

# Path params
directory_name = "temp"
if not os.path.exists(directory_name):
        os.makedirs(directory_name)

def visualize_initial(points):
    title = "Initial Points"

    file_name = title.lower().replace(" ", "_") + ".png"
    file_path = os.path.join(directory_name, file_name)

    plt.figure(figsize=(10, 10))

    # Отображение точек
    plt.scatter(points[:, 0], points[:, 1], s=20, color='lightblue')

    plt.title(title)
    plt.savefig(file_path)
    plt.show()


def visualize_clusters(points, clusters, title, centroids=None, medoids=None):
    file_name = title.lower().replace(" ", "_") + ".png"
    file_path = os.path.join(directory_name, file_name)

    plt.figure(figsize=(10, 10))

    cluster_ids = list(clusters.keys())
    num_clusters = len(cluster_ids)
    colors = plt.get_cmap('tab20', num_clusters)

    cluster_to_color_index = {cluster_id: idx for idx, cluster_id in enumerate(cluster_ids)}

    print(f"Visualizing {num_clusters} clusters...")

    # Отображение точек кластеров
    for cluster_id in cluster_ids:
        point_indices = clusters[cluster_id]
        cluster_points = points[point_indices]
        color_idx = cluster_to_color_index[cluster_id]
        print(f"Cluster {cluster_id}, Points {len(cluster_points)}")
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], s=20, color=colors(color_idx))

    print("Done")

    # Отображение центроидов
    if centroids is not None:
        print("Drawing centroids...")

        for cluster_id, centroid in centroids.items():
            color_idx = cluster_to_color_index[cluster_id]
            print(f"Centroid {cluster_id}")
            plt.scatter(centroid[0], centroid[1], s=20, color=colors(color_idx), edgecolor='black')

        print("Done")

    # Отображение медоидов
    if medoids is not None:
        print("Drawing medoids...")

        for cluster_id, medoid in medoids.items():
            color_idx = cluster_to_color_index[cluster_id]
            print(f"Medoid {cluster_id}")
            plt.scatter(medoid[0], medoid[1], s=20, color=colors(color_idx), edgecolor='black')

        print("Done")

    plt.title(title)
    plt.savefig(file_path)
    plt.show()
