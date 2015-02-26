#!/usr/bin/env python
# encoding: utf-8


def split_by_5_minute(time_col):
    day_hour = time_col[6:10]
    miniute = int(time_col[10:12]) / 5 * 5
    return day_hour + ('%02d' % miniute)
