#!/usr/bin/env python
# encoding: utf-8

import json
import pandas as pd
from collections import Counter

cols = ['gps', 'desc', 'amap', 'data']

tag_blacklist = set(['地名地址信息', '交通地名',
                     '路口名', '热点地名', '桥', '区县级地名',
                     '普通地名', '出入口', '楼栋号',
                     '高速路入口', '门牌信息',
                     '商务住宅', '楼宇'])


def get_semantic_description(data):
    try:
        return data["regeocode"]["formatted_address"]
    except:
        return None


def get_business(data):
    result = []
    try:
        for area in data["regeocode"]["addressComponent"]["businessAreas"]:
            result.append(area['name'])
        return ' '.join(result)
    except:
        return None


def get_district(data):
    try:
        return data["regeocode"]["addressComponent"]["district"]
    except:
        return None


def get_semantic_tags(data):
    counter = {}
    try:
        tag = data["regeocode"]["addressComponent"]["neighborhood"]["type"].split(";")[1]
        if tag.encode('utf8') not in tag_blacklist:
            counter.setdefault(tag, 0)
            counter[tag] += 1
    except:
        pass
    try:
        tag = data["regeocode"]["addressComponent"]["building"]["type"].split(";")[1]
        if tag.encode('utf8') not in tag_blacklist:
            counter.setdefault(tag, 0)
            counter[tag] += 1
    except:
        pass

    for poi in data["regeocode"]['pois']:
        poi_type = poi['type']
        tag = poi_type.split(";")[1]
        if tag.encode('utf8') not in tag_blacklist:
            counter.setdefault(tag, 0)
            counter[tag] += float(poi['poiweight'])
    sorted_pairs = sorted(counter.items(), key=lambda x: -x[1])
    return ' '.join(['%s:%.3f' % (k.replace(' ', '_'), v) for k, v in sorted_pairs])


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
