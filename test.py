import matplotlib.pyplot as plt
import random
import numpy as np
from gen_map import read_data_files
from visualize_tsp import plotTSP
from tools import city_distance, calc_path_distance

# ============================================================
# [readme]
# test file is used for verifying your output "result.txt"
# run ``python test.py"
# if it failed or cannot produce 3 scores as final results
# you should check your code

# [warning]
# make sure your result.txt can pass the test and produce 3 scores

# make sure that you DO NOT change anything in this test file
# any violation of this policy leads to the failed project
# don't submit train.py and test.py; just submit tsp.py
# ============================================================

if __name__ == "__main__":

    # read in maps
    all_test_coords = read_data_files()

    # read in your generated paths
    with open('result.txt', 'r') as f:
        all_test_path_string = f.readlines()

    # make sure they have same number of records
    assert len(all_test_path_string) == len(all_test_coords)

    all_dist = []
    for ix in range(len(all_test_coords)):
        coords, path_string  = all_test_coords[ix], all_test_path_string[ix]
        # convert path string to list of index
        path = list(map(int, path_string.strip().split()))
        # make sure the path length is number of nodes plus 1 (back to starting point)
        assert len(path)==len(coords)+1
        # come back to starting point 0
        assert path[0] == path[-1] == 0
        # no circle
        assert len(set(path)) == len(coords)
        # no invalid index
        assert max(path)+1==len(path)-1
        # calculate your total path distance
        distance_matrix = city_distance(coords)
        dist = calc_path_distance(distance_matrix, path)
        all_dist.append(dist)

        if 1==1:
            # turn this on (1==1) if you want to visualize your solution
            plotTSP(path,coords,1)

    for ix, dist in enumerate(all_dist):
        print('Path %d: %.2f' % (ix, dist))



