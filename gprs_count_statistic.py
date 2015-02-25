#!/usr/bin/env python
# encoding: utf-8

"""
统计每个用户每天以(半小时/一小时)粒度的请求数量
"""

from csv import DictReader
from csv import DictWriter
from collections import Counter
from constants import log_header
import os
import logging

logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.DEBUG)


field_name = 'start_time'


def split_by_hour(time_col):
    return time_col[6:10]


def split_by_halfhour(time_col):
    date = time_col[6:8]
    hour = int(time_col[8:10])
    miniute = int(time_col[10:12])
    over_half = 1 if int(miniute) >= 30 else 0
    return date + ('%02d' % (hour * 2 + over_half))


def gprs_statistic(fileobj, split_func):
    reader = DictReader(fileobj, fieldnames=log_header)
    counter = Counter()
    for row in reader:
        counter[split_func(row[field_name])] += 1
    return counter


def save_to_csv(fileobj, uid, counter):
    writer = DictWriter(fileobj, fieldnames=['uid', 'time', 'request_count'])
    for split_time, count in counter.iteritems():
        writer.writerow({'uid': uid, 'time': split_time, 'request_count': count})


def get_uid(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]


if __name__ == '__main__':
    import sys
    import glob
    import time

    start = time.time()

    inputdir = sys.argv[1]
    outputfile = sys.argv[2]
    split_type = int(sys.argv[3])
    split_func = split_by_hour if split_type == 1 else split_by_halfhour

    csvfiles = glob.glob(os.path.join(inputdir, '*', '*.csv'))
    n = len(csvfiles)
    if os.path.isfile(outputfile):
        os.remove(outputfile)

    with open(outputfile, 'a') as outputfileobj:
        for idx, csvfile in enumerate(csvfiles):
            uid = get_uid(csvfile)
            with open(csvfile) as f:
                counter = gprs_statistic(f, split_func)
            save_to_csv(outputfileobj, uid, counter)
            logging.info('[%d/%d]' % (idx + 1, n))

    logging.info('finish with time %s', str(time.time() - start))
