#!/usr/bin/env python
# encoding: utf-8

import numpy as np
from constants import clean_log_header
import csv
from common import date_parser
from common import create_dir_if_not_exists
import logging
from collections import defaultdict
import glob
import os

logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.DEBUG)


location_idx = clean_log_header.index('location')
day_idx = clean_log_header.index('day')
lat_idx = clean_log_header.index('latitude')
lon_idx = clean_log_header.index('longitude')
start_time_idx = clean_log_header.index('start_time')
duration_idx = -3
distance_idx = -2
speed_idx = -1


def cal_est_distance(lon1, lat1, lon2, lat2):
    rate = 97
    return rate * np.sqrt((lon1 - lon2) ** 2 + (lat1 - lat2) ** 2) * 1.4


def group_by_day(lines):
    results = defaultdict(list)
    for line in lines:
        results[int(line[day_idx])].append(line)
    return results


def cal_speed(csvs):
    last_start_time = None
    last_lat = None
    last_lon = None
    for idx, line in enumerate(csvs):
        lat = float(line[lat_idx])
        lon = float(line[lon_idx])
        start_time = date_parser(line[start_time_idx])
        if idx == 0:
            # time
            line.append(0)
            # distance
            line.append(0)
            # speed
            line.append(0)
        else:
            # time
            duration = start_time - last_start_time
            line.append(duration.seconds)
            line.append(cal_est_distance(lon, lat, last_lon, last_lat))
            line.append(line[-1] / (line[-2] + 120) * 3600)

        last_start_time = start_time
        last_lat = lat
        last_lon = lon

    return csvs


def pickout_invalid_points(csvs, speed_thresh=300):
    invalid_locations = set()
    last_location = None

    for idx, line in enumerate(csvs):
        speed = line[speed_idx]
        if speed > speed_thresh:
            if last_location not in invalid_locations:
                invalid_locations.add(line[location_idx])
        last_location = line[location_idx]

    newlines = [line for line in csvs
                if line[location_idx] not in invalid_locations]

    return invalid_locations, newlines


def write_invalid_points(dstdir, uid, invalid_points):
    with open(os.path.join(dstdir, uid + '.point'), 'w') as ofile:
        for point in invalid_points:
            ofile.write("%s\n" % point)


def per_file(filepath, dstfilepath, dstdir, uid, speed_thresh):
    with open(filepath, 'rb') as ifile:
        csvreader = csv.reader(ifile)
        lines = list(csvreader)

    lines = sorted(lines, key=lambda x: x[start_time_idx])
    groupbyday = group_by_day(lines)

    results = []
    invalid_locations = set()
    for day in range(1, 32):
        if day not in groupbyday:
            continue
        lines = groupbyday[day]
        # logging.info('Lines: %d of %d', len(lines), day)
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


def main(src_dir, dst_dir, speed_thresh):
    files = glob.glob(os.path.join(src_dir, '*', '*.csv'))
    total_file_cnt = len(files)

    for cnt, csvfile in enumerate(files):
        logging.info('[%d/%d] processing: %s',
                     cnt + 1, total_file_cnt, csvfile)
        uid = os.path.splitext(os.path.basename(csvfile))[0]
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
    main(src_dir, dst_dir, speed_thresh)
