#!/usr/bin/env python
# encoding: utf-8

import json
import pandas as pd
from collections import Counter

cols = ['gps', 'desc', 'baidu', 'data']


def get_semantic_description(data):
    return data['result']['sematic_description']


def get_business(data):
    return data['result']['business']


def get_district(data):
    return data['result']["addressComponent"]['district']


def get_semantic_tags(data):
    result = []
    for poi in data['result']['pois']:
        name = poi['name']
        poi_type = poi['poiType']
        result.append((name, poi_type))
    return ' '.join(['%s:%s' % (k, v) for k, v in result])


def main(inputfile, outputfile):
    df = pd.read_csv(inputfile, names=cols)
    df['data'] = df['data'].map(lambda data: json.loads(data.replace(r'\"', '"').replace('\\', '\\\\')))
    df['tags'] = df['data'].map(get_semantic_tags)
    df['semantic_description'] = df['data'].map(get_semantic_description)
    df['business'] = df['data'].map(get_business)
    df['district'] = df['data'].map(get_district)
    del df['data']
    df.to_csv(outputfile, header=None, index=None, encoding='utf8')


if __name__ == '__main__':
    import sys
    inputfilepath = sys.argv[1]
    outputfilepath = sys.argv[2]

    with open(inputfilepath) as inputfile:
        outputfile = open(outputfilepath, 'w')
        main(inputfile, outputfile)
        outputfile.close()
