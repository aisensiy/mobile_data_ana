#!/usr/bin/env python
# encoding: utf-8

import os
import pandas as pd
import numpy as np
from datetime import datetime
import StringIO


def load_file(redis_server, filepath):
    value = redis_server.get(filepath)
    if value:
        print 'In redis!'
        return StringIO.StringIO(value)
    else:
        return open(filepath, buffering=(2 << 25))


def create_dir_if_not_exists(dst_dir):
    if not os.path.isdir(dst_dir):
        os.mkdir(dst_dir)


def get_uid(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]


def add_postfix(filename, postfix):
    filepath, fileext = os.path.splitext(filename)
    return filepath + '.' + postfix + fileext


def date_parser(date_str):
    return datetime.strptime(date_str, '%Y%m%d%H%M%S')


def date_formater(date):
    return date.strftime('%Y%m%d%H%M%S')


def prepare_dataframe(filepath, header=None):
    """@todo: 准备待处理的DataFrame, 包括解析时间, 生成字段,
       排序, 重置索引, 坐标格式化".5f"

    :filepath:
    :returns: DataFrame

    """
    df = pd.read_csv(filepath, header=None, names=header,
                     dtype={'start_time': np.str},
                     na_values=set(['', None]))

    cur_len = len(df)
    df = df[(df.start_time.notnull()) &
            (df.latitude.notnull()) & (df.longitude.notnull())]
    cur_len_without_na = len(df)
    if cur_len != cur_len_without_na:
        print 'remove na rows: %d' % (cur_len - cur_len_without_na)

    df.start_time = df.start_time.map(date_parser)

    df['longitude'] = df.longitude.map(lambda x: '%.5f' % x)
    df['latitude'] = df.latitude.map(lambda x: '%.5f' % x)
    df['location'] = zip(df.longitude, df.latitude)
    df['date'] = df.start_time.map(lambda x: x.strftime('%Y-%m-%d'))

    df.set_index('start_time', inplace=True)
    df.sort_index(inplace=True)

    return df
