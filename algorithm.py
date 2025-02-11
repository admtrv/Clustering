# algorithm.py

import config
from evaluation import evaluate_clustering
from generation import generate_initial_points, generate_additional_points
from centroids import agglomerative_centroid_clustering
from medoids import agglomerative_medoid_clustering
from visualization import visualize_clusters, visualize_initial

# Config data
additional_points_num = config.additional_points_num
additional_points_num_medoid = config.additional_points_num_medoid
clusterization_method = config.clusterization_method

if __name__ == "__main__":

    print("Generating points...")
    initial_points = generate_initial_points()

    if clusterization_method == "centroid_clustering":
        all_points = generate_additional_points(initial_points, additional_points_num)
        print("Done")
        print(f"Initial points {len(all_points)}")
        visualize_initial(all_points)

        clusters, centroids = agglomerative_centroid_clustering(all_points)
        visualize_clusters(all_points, clusters, 'Centroids', centroids=centroids)
        evaluate_clustering(all_points, clusters, centroids)

    elif clusterization_method == "medoid_clustering":
        all_points = generate_additional_points(initial_points, additional_points_num_medoid)
        print("Done")
        print(f"Initial points {len(all_points)}")
        visualize_initial(all_points)

        clusters, medoids = agglomerative_medoid_clustering(all_points)
        visualize_clusters(all_points, clusters, 'Medoids', medoids=medoids)
        evaluate_clustering(all_points, clusters, medoids)

    elif clusterization_method == "unify_clustering":
        all_points = generate_additional_points(initial_points, additional_points_num)
        print("Done")
        print(f"Initial points {len(all_points)}")
        visualize_initial(all_points)

        clusters, centroids = agglomerative_centroid_clustering(all_points)
        visualize_clusters(all_points, clusters, 'Centroids', centroids=centroids)
        evaluate_clustering(all_points, clusters, centroids)

        clusters, medoids = agglomerative_medoid_clustering(all_points)
        visualize_clusters(all_points, clusters, 'Medoids', medoids=medoids)
        evaluate_clustering(all_points, clusters, medoids)