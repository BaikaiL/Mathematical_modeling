'''
Distance calculator.
Do not modify.
'''
import math
from math import radians, cos, sin, asin, sqrt
import numpy as np

# calculate pairwise city distance on earth
def city_distance(cities):
    N = len(cities)
    distance_matrix = np.zeros((N,N))
    for i in range(N):
        loni, lati = cities[i]
        for j in range(i,N):
            lonj, latj = cities[j]
            dist = earth_distance(loni,lati,lonj,latj)
            distance_matrix[i][j] = distance_matrix[j][i] = dist

    distance_matrix=np.round(distance_matrix, 2)
    return distance_matrix

# calculate earth distance
# input 经度1，纬度1，经度2，纬度2 （十进制度数）
def earth_distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r

def calc_path_distance(distance_matrix, solution):
    """
    Total distance of the current solution path.
    """
    N = distance_matrix.shape[0]
    cur_dist = 0
    for i in range(N):
        cur_dist += distance_matrix[solution[i % N], solution[(i + 1) % N]]
    return cur_dist
