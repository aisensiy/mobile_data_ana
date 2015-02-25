#!/usr/bin/env python
# encoding: utf-8

"""
统计每个用户每天以(半小时/一小时)粒度的请求数量
"""

from csv import DictReader
from csv import DictWriter
from collections import Counter
from constants import log_header


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
    for time, count in counter.iteritems():
        writer.writerow({'uid': uid, 'time': time, 'request_count': count})
