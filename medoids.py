# medoids.py

import numpy as np
import time

import config
max_average_distance = config.max_average_distance

def agglomerative_medoid_clustering(points):
    return points