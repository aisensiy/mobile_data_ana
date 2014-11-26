#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
from constants import noinvalid_clean_log_header as cols
from common import prepare_dataframe
import os
import glob
import logging
from datetime import datetime
from collections import Counter
import json

logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.DEBUG)
start_at = datetime.now()


def costs():
    delta = datetime.now() - start_at
    return '%02d:%02d:%02d' % (delta.seconds / 3600,
                               delta.seconds % 3600 / 60,
                               delta.seconds % 60)


def location_and_app_stat(filepath, columns):
    df = pd.read_csv(filepath, header=None, names=columns)
    avg_cnt_per_day = df.groupby('day').size().mean()
    cnt_of_day = df.day.nunique()
    cnt_of_app = df.busi_name.nunique()
    avg_app_per_day = df.groupby('day') \
        .agg({'busi_name': lambda x: x.nunique()})['busi_name'].mean()
    avg_location_per_day = df.groupby('day') \
        .agg({'location': lambda x: x.nunique()})['location'].mean()
    cnt_of_location = df.location.nunique()
    cnt_of_lac = df.lac.nunique()
    stat = pd.DataFrame({
        'user_id': [df.user_id[0]],
        'req_cnt': [len(df)],
        'request_avg_per_day': [avg_cnt_per_day],
        'request_day': [cnt_of_day],
        'app_count': [cnt_of_app],
        'app_avg_per_day': [avg_app_per_day],
        'location_avg_per_day': [avg_location_per_day],
        'location_count': [cnt_of_location],
        'locations': [json.dumps(Counter(df.location.tolist()))],
        'lac_count': [cnt_of_lac]
    })
    return stat


def get_all_stats(dirpath, dstfilepath):
    dfs = []
    if not os.path.isdir(dirpath):
        logging.debug('No dir %s' % dirpath)
        return

    files = glob.glob(os.path.join(dirpath, '*', '*.csv'))
    total_file_cnt = len(files)
    for cnt, csvfile in enumerate(files):
        logging.info('[%d/%d] processing: %s costs: %s',
                     cnt + 1, total_file_cnt, csvfile, costs())
        df = location_and_app_stat(csvfile, cols)
        dfs.append(df)

    result = pd.concat(dfs, ignore_index=True)
    logging.info('save to %s' % dstfilepath)
    result.to_csv(dstfilepath, index=False)

    return dfs

if __name__ == '__main__':
    import sys

    dirpath = sys.argv[1]
    dstfile = sys.argv[2]

    dfs = get_all_stats(dirpath, dstfile)
