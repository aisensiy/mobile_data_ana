#!/usr/bin/env python
# encoding: utf-8

import os
import logging
import glob
import csv
from common import create_dir_if_not_exists
from constants import log_header as raw_log_header
from datetime import datetime


logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.DEBUG)

start_at = datetime.now()


def costs():
    delta = datetime.now() - start_at
    return '%02d:%02d:%02d' % (delta.seconds / 3600,
                               delta.seconds % 3600 / 60,
                               delta.seconds % 60)


def clean_data(filepath, dst_filepath, header):
    """
    1. remove row with start_time latitude longitude is null
    2. format location
    3. add column location hour and day
    """
    latitude_idx = header.index('latitude')
    longitude_idx = header.index('longitude')
    start_time_idx = header.index('start_time')

    with open(filepath, 'rb') as csv_file:
        csvreader = csv.reader(csv_file)
        outputfile = open(dst_filepath, 'wb')
        csvwriter = csv.writer(outputfile)
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
            row.append(row[start_time_idx][8:10])
            row.append(row[start_time_idx][10:12])

            csvwriter.writerow(row)

        outputfile.close()

    if origin_len != cleaned_len:
        logging.debug('remove na rows: %d' % (origin_len - cleaned_len))


def main(src_dir, dst_dir, valid_user_file):
    create_dir_if_not_exists(dst_dir)
    csv_files = glob.glob(os.path.join(src_dir, '*', '*.csv'))
    total_file_cnt = len(csv_files)
    valid_users = set(map(lambda x: x.strip(),
                          open(valid_user_file).readlines()))
    for cnt, csv_file in enumerate(csv_files):
        logging.info('[%d/%d] processing: %s costs: %s',
                     cnt + 1, total_file_cnt, csv_file, costs())
        filename = os.path.basename(csv_file)
        dirname = os.path.splitext(filename)[0][-2:]
        uid = os.path.splitext(filename)[0]
        if uid not in valid_users:
            continue
        create_dir_if_not_exists(os.path.join(dst_dir, dirname))
        dst_csv_file = os.path.join(dst_dir, dirname, filename)
        clean_data(csv_file, dst_csv_file, raw_log_header)


if __name__ == '__main__':
    import sys
    src_dir = sys.argv[1]
    dst_dir = sys.argv[2]
    main(src_dir, dst_dir, 'valid_users.csv')
