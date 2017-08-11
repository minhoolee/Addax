import json
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import pickle

dataset = list()

def calc_view_max():
    v_max = 0
    for e in dataset:
        v = e['view_count']
        if v > v_max:
            v_max = v
    return v_max

def calc_impact_scores():
    v_max = calc_view_max()
    a = []
    i_mean = 0
    for e in dataset:
        l = e['like_count']
        d = e['dislike_count']
        v = e['view_count']
        e['impact_score'] = (float((l-d))/(l+d) + float(v) / v_max)
        a.append(e['impact_score'])
    min_val = min(a)
    max_val = max(a)
    a = [(x - min_val)/(max_val - min_val) for x in a]

    for i in range(len(dataset)):
        dataset[i]['impact_score'] = a[i]

def save_as_hdf5(target):
    with open(target, 'wb') as f:
        pickle.dump(dataset, f)

def parse(dir, target):
    for f in glob.glob(dir + '/*.json'):
        with open(f, 'r') as infile:
            s = json.load(infile)
            entry = dict([
                ('like_count', s['like_count']),
                ('dislike_count', s['dislike_count']),
                ('title', s['title']),
                ('uploader', s['uploader']),
                ('view_count', s['view_count']),
                ('duration', s['duration'])
            ])
            dataset.append(entry)
    calc_impact_scores()
    save_as_hdf5(target)

def main(argv):
    parse(argv[0], argv[1])

if __name__ == '__main__':
    main(sys.argv[1:])
