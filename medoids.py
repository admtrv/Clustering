# medoids.py

import numpy as np
import time

import config
max_average_distance = config.max_average_distance

def agglomerative_medoid_clustering(points):
    num_points = len(points)
    clusters = {i: [i] for i in range(num_points)}  # Словарь, где индекс - это кластер
    medoids = {i: points[i].astype(float) for i in range(num_points)}  # Словарь, где индекс - это координаты медоида

    print("Destination matrix initialization...")
    distance_matrix = np.full((num_points, num_points), np.inf)  # Матрица расстояний между парами точек
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

    active_clusters = set(range(num_points))  # Множество всех активных кластеров

    iteration = 0
    total_start_time = time.time()

    print("Cycle of clusterization...")
    while len(active_clusters) > 1:  # Активный кластер — это кластер, который ещё участвует в процессе
        iteration += 1

        min_distance = np.inf
        min_pair = None

        for i in active_clusters:  # Поиск ближайшей пары кластеров
            distances = distance_matrix[i, list(active_clusters)]
            min_idx = np.argmin(distances)
            j = list(active_clusters)[min_idx]
            if i != j and distance_matrix[i, j] < min_distance:
                min_distance = distance_matrix[i, j]  # Пара кластеров для объединения
                min_pair = (i, j)

        if min_pair is None:
            print(f"Iteration {iteration}, can't find pair to unite")
            break

        i, j = min_pair

        if min_distance > max_average_distance:
            print(f"Iteration {iteration}, stopping as min_distance ({min_distance:.2f}) > max_average_distance ({max_average_distance})")
            break

        print(f"Iteration {iteration}, Uniting clusters {i} {j}, Distance {min_distance:.2f}")

        # Объединяем кластеры i и j
        clusters[i].extend(clusters[j])  # Добавляем точки из j в i
        del clusters[j]  # Удаляем j из словаря и множества активных кластеров
        active_clusters.remove(j)
        del medoids[j]

        # Обновляем медоид кластера i
        # Медоид — точка внутри кластера, которая минимизирует сумму расстояний до всех остальных точек кластера
        cluster_points = [points[idx] for idx in clusters[i]]
        min_sum_distance = np.inf
        new_medoid = medoids[i]
        for point in cluster_points:
            sum_distance = np.sum([np.linalg.norm(point - other_point) for other_point in cluster_points])
            if sum_distance < min_sum_distance:
                min_sum_distance = sum_distance
                new_medoid = point
        medoids[i] = new_medoid

        # Обновляем матрицу расстояний для кластера i
        for k in active_clusters:
            if k != i:
                dist = np.linalg.norm(medoids[i] - medoids[k])  # Расстояние от нового медоида до остальных активных кластеров
                distance_matrix[i, k] = dist
                distance_matrix[k, i] = dist

    print("Done")

    total_time = time.time() - total_start_time
    print(f"Total time {total_time:.2f} s, Iterations {iteration}")

    return clusters, medoids