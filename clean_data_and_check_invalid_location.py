#!/usr/bin/env python
# encoding: utf-8

"""
硬盘有限，一次性完成清理数据与异常点剔除的工作
"""

import os
import logging
import glob
import csv
from common import create_dir_if_not_exists
from constants import log_header as raw_log_header
from constants import clean_log_header
from check_invalid_location import group_by_day
from check_invalid_location import pickout_invalid_points
from check_invalid_location import cal_speed
from check_invalid_location import write_invalid_points
from datetime import datetime


logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.DEBUG)

start_at = datetime.now()
start_time_idx = clean_log_header.index('start_time')


def costs():
    delta = datetime.now() - start_at
    return '%02d:%02d:%02d' % (delta.seconds / 3600,
                               delta.seconds % 3600 / 60,
                               delta.seconds % 60)


def clean_data(filepath, header):
    """
    1. remove row with start_time latitude longitude is null
    2. format location
    3. add column location hour and day
    """
    latitude_idx = header.index('latitude')
    longitude_idx = header.index('longitude')
    start_time_idx = header.index('start_time')

    output = []

    with open(filepath, 'rb') as csv_file:
        csvreader = csv.reader(csv_file)
        origin_len = 0
        cleaned_len = 0
        for row in csvreader:
            origin_len += 1
            if row[latitude_idx] == '' or row[longitude_idx] == '' or row[start_time_idx] == '':
                continue
            cleaned_len += 1
            row[latitude_idx] = '%.5f' % float(row[latitude_idx])
            row[longitude_idx] = '%.5f' % float(row[longitude_idx])
            row.append(row[latitude_idx] + ' ' + row[longitude_idx])
            row.append(row[start_time_idx][6:8])
            row.append(row[start_time_idx][8:10])

            output.append(row)

    if origin_len != cleaned_len:
        logging.debug('remove na rows: %d - %d = %d' %
                      (origin_len, cleaned_len, origin_len - cleaned_len))

    return output


def per_file(filepath, dstfilepath, dstdir, uid, speed_thresh):
    cleaned_csvs = clean_data(filepath, raw_log_header)
    if len(cleaned_csvs) == 0:
        return

    lines = sorted(cleaned_csvs, key=lambda x: x[start_time_idx])
    groupbyday = group_by_day(lines)

    results = []
    invalid_locations = set()
    for day in range(1, 32):
        if day not in groupbyday:
            continue
        lines = groupbyday[day]
        lines = cal_speed(lines)
        locations, lines = pickout_invalid_points(lines, speed_thresh)
        results += lines
        invalid_locations = invalid_locations | locations

    # logging.info('Lines: %d', len(results))
    with open(dstfilepath, 'wb') as ofile:
        writer = csv.writer(ofile)
        for line in results:
            writer.writerow(line)

    write_invalid_points(dstdir, uid, invalid_locations)


def main(src_dir, dst_dir, valid_user_file, speed_thresh):
    files = glob.glob(os.path.join(src_dir, '*', '*.csv'))
    total_file_cnt = len(files)
    valid_users = set(map(lambda x: x.strip(),
                          open(valid_user_file).readlines()))

    for cnt, csvfile in enumerate(files):
        logging.info('[%d/%d] processing: %s costs: %s',
                     cnt + 1, total_file_cnt, csvfile, costs())
        uid = os.path.splitext(os.path.basename(csvfile))[0]
        if uid not in valid_users:
            continue
        dstdir = os.path.join(dst_dir, uid[-2:])
        create_dir_if_not_exists(dstdir)
        dstfile = os.path.join(dstdir, uid + '.csv')
        if os.path.isfile(dstfile):
            continue
        per_file(csvfile, dstfile, dstdir, uid, speed_thresh)


if __name__ == '__main__':
    import sys
    src_dir = sys.argv[1]
    dst_dir = "%s-no-invalidpoint" % src_dir
    speed_thresh = int(sys.argv[2]) if len(sys.argv) >= 3 else 300
    create_dir_if_not_exists(dst_dir)
    main(src_dir, dst_dir, 'valid_users.csv', speed_thresh)
    end_at = datetime.now()
    delta = end_at - start_at
