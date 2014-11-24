#!/usr/bin/env python
# encoding: utf-8

"""
get some key info from the json data
"""


import pandas as pd
import json
from collections import Counter


def get_street(data):
    try:
        return data['result']['addressComponent']['street'].encode('utf8')
    except:
        return ""


def get_business(data):
    try:
        return data['result']['business'].encode('utf8')
    except:
        return ""


def get_address(data):
    try:
        return data['result']['formatted_address'].encode('utf8')
    except:
        return ""


def get_distinct(data):
    try:
        return data['result']['addressComponent']['district'].encode('utf8')
    except:
        return ""


def get_tags(data):
    try:
        tags = []
        for poi in data['result']['pois']:
            tags.append(poi['poiType'])
        return ",".join(tags).encode('utf8')
    except:
        return ""


def main(src, dst):
    df = pd.read_csv(src, header=None)
    df['location'] = df[0].map(
        lambda x: '%.3f %.4f' % tuple(reversed(map(float, x.split(' ')))))
    df['json'] = df[1].map(lambda x: json.loads(x))
    df['street'] = df['json'].map(get_street)
    df['business'] = df['json'].map(get_business)
    df['address'] = df['json'].map(get_address)
    df['distinct'] = df['json'].map(get_distinct)
    df['tags'] = df['json'].map(get_tags)
    del df['json']
    del df[0]
    df.to_csv(dst, index=None, header=None)


if __name__ == '__main__':
    import sys
    src = sys.argv[1]
    dst = sys.argv[2]
    main(src, dst)
