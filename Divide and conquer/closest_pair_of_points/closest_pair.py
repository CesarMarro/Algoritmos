import math
import matplotlib.pyplot as plt


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def brute_force(points):
    min_dist = float("inf")
    pair = None
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
                pair = (points[i], points[j])
    return pair, min_dist


def strip_closest(strip, d):
    min_dist = d
    pair = None
    strip.sort(key=lambda p: p[1])  # Sort by y-coordinate
    n = len(strip)
    for i in range(n):
        for j in range(i + 1, n):
            if (strip[j][1] - strip[i][1]) < min_dist:
                dist = distance(strip[i], strip[j])
                if dist < min_dist:
                    min_dist = dist
                    pair = (strip[i], strip[j])
            else:
                break
    return pair, min_dist


def closest_util(points_sorted_x, points_sorted_y):
    n = len(points_sorted_x)
    if n <= 3:
        return brute_force(points_sorted_x)

    mid = n // 2
    midpoint = points_sorted_x[mid]

    left_x = points_sorted_x[:mid]
    right_x = points_sorted_x[mid:]

    left_y = list(filter(lambda p: p[0] <= midpoint[0], points_sorted_y))
    right_y = list(filter(lambda p: p[0] > midpoint[0], points_sorted_y))

    (left_pair, left_dist) = closest_util(left_x, left_y)
    (right_pair, right_dist) = closest_util(right_x, right_y)

    if left_dist < right_dist:
        d = left_dist
        min_pair = left_pair
    else:
        d = right_dist
        min_pair = right_pair

    strip = [p for p in points_sorted_y if abs(p[0] - midpoint[0]) < d]
    strip_pair, strip_dist = strip_closest(strip, d)

    if strip_dist < d:
        return strip_pair, strip_dist
    else:
        return min_pair, d


def closest_pair(points):
    points_sorted_x = sorted(points, key=lambda p: p[0])
    points_sorted_y = sorted(points, key=lambda p: p[1])
    return closest_util(points_sorted_x, points_sorted_y)


# Simulación y visualización
import random


def simulate_closest_pair():
    num_points = 100
    points = [
        (random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_points)
    ]

    closest_points, min_dist = closest_pair(points)
    print(f"Par más cercano: {closest_points} con una distancia de {min_dist}")

    # Graficar los puntos
    x_vals, y_vals = zip(*points)
    plt.scatter(x_vals, y_vals, label="Puntos")

    # Graficar el par más cercano
    plt.plot(
        [closest_points[0][0], closest_points[1][0]],
        [closest_points[0][1], closest_points[1][1]],
        color="red",
        label="Par más cercano",
    )

    plt.legend()
    plt.title("Closest Pair of Points")
    plt.show()


simulate_closest_pair()
