# centroids.py

import numpy as np
import time

import config
max_average_distance = config.max_average_distance

def agglomerative_centroid_clustering(points):
    num_points = len(points)
    clusters = {i: [i] for i in range(num_points)}                          # Cловарь индекс - отдельный кластер
    centroids = {i: points[i].astype(float) for i in range(num_points)}     # Cловарь индекс - координаты соответствующего центроида

    print("Destination matrix initialization...")
    distance_matrix = np.full((num_points, num_points), np.inf)      # Матрица расстояний между парами точек
    start_time = time.time()
    for i in range(num_points):

        if i % 1000 == 0 or i == num_points - 1:
            elapsed_time = time.time() - start_time
            print(f"Processed {i + 1}/{num_points} points, Time {elapsed_time:.2f} s")

        for j in range(i + 1, num_points):
            dist = np.linalg.norm(points[i] - points[j])
            distance_matrix[i, j] = dist
            distance_matrix[j, i] = dist
    print("Done")

    active_clusters = set(range(num_points))    # Множество всех активных кластеров

    iteration = 0
    total_start_time = time.time()

    print("Cycle of clusterization...")
    while len(active_clusters) > 1:             # Активный кластер — кластер, который ещё участвует в процессе
        iteration += 1

        min_distance = np.inf
        min_pair = None

        for i in active_clusters:                                   # Поиск ближайшей пары кластеров
            distances = distance_matrix[i, list(active_clusters)]
            min_idx = np.argmin(distances)
            j = list(active_clusters)[min_idx]
            if i != j and distance_matrix[i, j] < min_distance:
                min_distance = distance_matrix[i, j]                # Пара кластеров для объединения
                min_pair = (i, j)


        if min_pair is None:
            print(f"Iteration {iteration}, cant find pair to unite")
            break

        i, j = min_pair

        if min_distance > max_average_distance:
            print(f"Iteration {iteration}, stopping as min_distance ({min_distance:.2f}) > max_average_distance ({max_average_distance})")
            break

        print(f"Iteration {iteration}, Uniting clusters {i} {j}, Distance {min_distance:.2f}")

        # Объединяем кластеры i и j
        clusters[i].extend(clusters[j])     # Добавляем точки из j в i
        del clusters[j]                     # Удаляем j из словаря и активного множества
        active_clusters.remove(j)
        del centroids[j]

        # Обновляем центроид кластера i
        centroids[i] = np.mean(points[clusters[i]], axis=0)         # Среднее арифметическое координат всех точек

        # Обновляем матрицу расстояний для кластера i
        for k in active_clusters:
            if k != i:
                dist = np.linalg.norm(centroids[i] - centroids[k])      # Расстояние от нового кластера до остальных активных кластеров
                distance_matrix[i, k] = dist
                distance_matrix[k, i] = dist

    print("Done")

    total_time = time.time() - total_start_time
    print(f"Total time {total_time:.2f} s, Iterations {iteration}")

    final_centroids = {cluster_id: centroids[cluster_id] for cluster_id in clusters.keys()}

    return clusters, centroids