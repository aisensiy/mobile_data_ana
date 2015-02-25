#!/usr/bin/env python
# encoding: utf-8

"""
统计每个用户每天以(半小时/一小时)粒度的请求数量
"""


def split_by_hour(time_col):
    return time_col[6:10]


def split_by_halfhour(time_col):
    date = time_col[6:8]
    hour = int(time_col[8:10])
    miniute = int(time_col[10:12])
    over_half = 1 if int(miniute) >= 30 else 0
    return date + ('%02d' % (hour * 2 + over_half))
