# generation.py

import numpy as np
import random
import config

# Config data
initial_points_num = config.initial_points_num
lower_bound = config.lower_bound
upper_bound = config.upper_bound
offset_range = config.offset_range

# Generation of initial few random points
def generate_initial_points():
    points = set()

    while len(points) < initial_points_num:
        x = random.randint(lower_bound, upper_bound)
        y = random.randint(lower_bound, upper_bound)

        points.add((x, y))

    return np.array(list(points))

# Generation of additional semi-random points
def generate_additional_points(initial_points, additional_points_num):
    points = initial_points.tolist()

    for _ in range(additional_points_num):
        it = random.randint(0, len(points) - 1)
        base_point = points[it]

        x_offset_lower = max(-offset_range, lower_bound - base_point[0])
        x_offset_upper = min(offset_range, upper_bound - base_point[0])
        y_offset_lower = max(-offset_range, lower_bound - base_point[1])
        y_offset_upper = min(offset_range, upper_bound - base_point[1])

        x_offset = random.randint(int(x_offset_lower), int(x_offset_upper))
        y_offset = random.randint(int(y_offset_lower), int(y_offset_upper))

        new_point = [base_point[0] + x_offset, base_point[1] + y_offset]

        points.append(new_point)

    return np.array(points)