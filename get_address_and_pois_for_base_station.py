#!/usr/bin/env python
# encoding: utf-8

"""
Input: file each line is longitude,latitude
Output: file with json data fetch from map.baidu.api
"""

import requests
import csv
import time
from constants import BAIDU_MAP_AK
import logging

logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.INFO)


def cal_offset(latitude, longitude):
    return float(latitude) + 0.007, float(longitude) + 0.013


def fetch_json_data(url):
    try:
        r = requests.get(url, timeout=10)
    except:
        r = None

    return r.text if r else None


def generate_url(latitude, longitude):
    latitude, longitude = cal_offset(latitude, longitude)
    return 'http://api.map.baidu.com/geocoder/v2/?ak=%s&location=%f,%f&output=json&pois=1' % (BAIDU_MAP_AK, latitude, longitude)


def main(src_file_path, dst_file_path, log_file_path):
    ofile = open(dst_file_path, 'wb')
    writer = csv.writer(ofile)
    logfile = open(log_file_path, 'w')
    with open(src_file_path, 'rb') as f:
        for line in f:
            longitude, latitude = line.strip().split(',')
            logging.info('fetching %s %s', latitude, longitude)
            time.sleep(0.1)
            url = generate_url(latitude, longitude)
            result = fetch_json_data(url)
            if not result:
                logfile.write("%s %s failed\n" % (latitude, longitude))
            writer.writerow([latitude + ' ' + longitude,
                             result.encode('utf8')])
    ofile.close()
    logfile.close()


if __name__ == '__main__':
    import sys
    src_file_path = sys.argv[1]
    dst_file_path = sys.argv[2]
    log_file_path = 'fetch_error.txt'
    main(src_file_path, dst_file_path, log_file_path)
