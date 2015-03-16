#!/usr/bin/env python
# encoding: utf-8

import logging
from csv import DictWriter
from csv import DictReader
from collections import Counter


logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.DEBUG)

cols = ['busi_name', 'busi_type_name', 'app_name', 'app_type_name',
        'site_name', 'site_channel_name', 'cont_app_id',
        'cont_classify_id', 'cont_type_id']

fieldnames = ['uid', 'minute'] + cols + ['domain', 'count']
keys = ['busi_name', 'busi_type_name', 'app_name', 'app_type_name',
        'site_name', 'site_channel_name', 'cont_app_id',
        'cont_classify_id', 'cont_type_id', 'domain']
target_fieldnames = keys + ['count']


def save_to_csv(writer, counter):
    for key, value in counter.most_common():
        row = dict(zip(target_fieldnames, list(key) + [value]))
        writer.writerow(row)


def unique_app_and_domain_statistic(fileobj, targetfileobj):
    reader = DictReader(fileobj, fieldnames=fieldnames)
    writer = DictWriter(targetfileobj, fieldnames=target_fieldnames)

    counter = Counter()

    for row in reader:
        key_data = tuple([row[key] for key in keys])
        counter[key_data] += int(row['count'])

    save_to_csv(writer, counter)


if __name__ == '__main__':
    import sys
    import time

    start = time.time()

    filepath = sys.argv[1]
    targetfilepath = sys.argv[2]

    target_obj = open(targetfilepath, 'w')
    with open(filepath, buffering=(2 << 25)) as f:
        unique_app_and_domain_statistic(f, target_obj)
    target_obj.close()
    logging.info('finish %s', str(time.time() - start))
