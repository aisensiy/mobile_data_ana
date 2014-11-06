#!/usr/bin/env python
# encoding: utf-8

"""
Input: file each line is longitude,latitude
Output: file with json data fetch from map.baidu.api
"""

import requests
import csv
from constants import BAIDU_MAP_AK
import logging

logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.INFO)


def fetch_json_data(url):
    r = requests.get(url)
    return r.text


def generate_url(latitude, longitude):
    return 'http://api.map.baidu.com/geocoder/v2/?ak=%s&location=%s,%s&output=json&pois=1' % (BAIDU_MAP_AK, latitude, longitude)


def main(src_file_path, dst_file_path):
    ofile = open(dst_file_path, 'wb')
    writer = csv.writer(ofile)
    with open(src_file_path, 'rb') as f:
        for line in f:
            longitude, latitude = line.strip().split(',')
            logging.info('fetching %s %s', latitude, longitude)
            url = generate_url(latitude, longitude)
            writer.writerow([latitude + ' ' + longitude,
                             fetch_json_data(url).encode('utf8')])
    ofile.close()


if __name__ == '__main__':
    import sys
    src_file_path = sys.argv[1]
    dst_file_path = sys.argv[2]
    main(src_file_path, dst_file_path)
