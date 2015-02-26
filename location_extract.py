#!/usr/bin/env python
# encoding: utf-8

from csv import DictReader
from csv import DictWriter
from time_helper import split_by_5_minute
import logging
from constants import log_header
from common import get_uid


logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.DEBUG)


def get_day_hour_minue(time_col):
    return time_col[6:-2]


def get_location(ln, la):
    return "%.5f %.5f" % (float(ln), float(la))


def prepare_user_log(fileobj):
    reader = DictReader(fileobj, fieldnames=log_header)
    rows = []
    for row in reader:
        if not row['longitude'] or not row['latitude']:
            continue
        location = get_location(row['longitude'], row['latitude'])
        rows.append({'start_time': row['start_time'],
                     'location': location})

    rows.sort(key=lambda x: (x['start_time'], x['location']))
    return rows


def extract_location(rows, split_func):
    last_location = None
    last_time_split = None
    location_logs = []

    for row in rows:
        cur_start_time = row['start_time']
        cur_location = row['location']
        cur_time_split = split_func(cur_start_time)

        if last_location is None or \
                last_location != cur_location or \
                last_time_split != cur_time_split:
            location_logs.append((cur_start_time, cur_location))

        last_location = cur_location
        last_time_split = cur_time_split

    return location_logs


def save_to_csv(fileobj, uid, logs):
    writer = DictWriter(fileobj, fieldnames=['uid', 'start_time', 'location'])
    for start_time, location in logs:
        writer.writerow({'uid': uid, 'start_time': start_time, 'location': location})


def main():
    import sys
    import glob
    import time
    import os

    start = time.time()

    inputdir = sys.argv[1]
    outputfile = sys.argv[2]
    valid_user_file = sys.argv[3]

    valid_users = set([line.strip() for line in open(valid_user_file)])
    split_func = split_by_5_minute

    csvfiles = glob.glob(os.path.join(inputdir, '*', '*.csv'))
    n = len(csvfiles)

    with open(outputfile, 'w') as outputfileobj:
        for idx, csvfile in enumerate(csvfiles):
            uid = get_uid(csvfile)
            if uid not in valid_users:
                continue
            with open(csvfile, buffering=(2 << 27)) as f:
                rows = prepare_user_log(f)
                logs = extract_location(rows, split_func)
            save_to_csv(outputfileobj, uid, logs)
            logging.info('[%d/%d]' % (idx + 1, n))

    logging.info('finish with time %s', str(time.time() - start))


if __name__ == '__main__':
    main()
