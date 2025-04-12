import os
import random
import numpy as np
from gen_map import read_data_files
from visualize_tsp import plotTSP
from tsp import my_wonderful_function
import argparse

# ============================================================
# [readme]
# this code will be executed to generate paths for 3 maps

# [warning]
# make sure that you DO NOT change anything in this train.py
# any cheating, plagiarism, letting others cheating,
# hard-coding paths, or other inappropriate academic behaviors
# will fail this project directly
# don't submit train.py and test.py; just submit tsp.py
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument('-n', '--no', type=int, default=1)
    args = parser.parse_args()

    group_num = args.no
    code_path = 'code/tsp_%d.py' % (group_num,)

    if not os.path.isfile(code_path):
        print('no code for group %d' % (group_num,))

    # this code line reads data_0~2.txt (3 maps) into array
    all_test_coords = read_data_files()

    # the main loop takes each map and executes your algorithm
    # then it should record the path and turn into a string line
    all_test_path_string = []
    for ix, coords in enumerate(all_test_coords):
        path_array = my_wonderful_function(coords)

        if 1 == 2:
            # turn this on (1==1) if you want to visualize your solution
            plotTSP(path_array, coords, 1)

        path_string = ' '.join(list(map(str, path_array)))  # list of coord index => string
        print('Path %d: %s' % (ix, path_string))
        all_test_path_string.append(path_string + "\n")

    # ----------------------------------------------------------
    # write the path string of each map into result.txt
    # check result.txt, make sure it's 3 lines of paths for 3 cases
    # do not modify the path or format.
    with open('result.txt', 'w') as f:
        f.writelines(all_test_path_string)
