'''
Data loader and coordinate generator.
Do not modify.
'''

NUM_FILE=3


def read_from_coords_txt(lines):
    data = []
    for line in lines:
        data.append(list(map(float,line.strip().split())))
    return data


def read_data_files(use_test=False):
    all_coords = []
    # read from data files, check they are the same
    for i in range(NUM_FILE):
        if use_test:
            with open('data/test_%d.txt' % (i,), 'r') as f:
                lines = f.readlines()
        else:
            with open('data/val_%d.txt' % (i,),'r') as f:
                lines = f.readlines()
                #print(lines)
        coords = read_from_coords_txt(lines)
        all_coords.append(coords)
    return all_coords

