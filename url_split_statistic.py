#!/usr/bin/env python
# encoding: utf-8

from csv import DictReader
from csv import DictWriter
from collections import Counter
import logging
from common import get_uid
from url_helper import get_top_domain
from constants import log_header
from time_helper import split_by_5_minute

logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.DEBUG)


def encode_domain_counter(counter):
    return "|".join(["%s:%d" % (domain, cnt)
                     for domain, cnt in counter.most_common()])


def domain_count_statistic(fileobj, split_func):
    reader = DictReader(fileobj, fieldnames=log_header)
    split_time_dict = {}
    for row in reader:
        time_split = split_by_5_minute(row['start_time'])
        domain = get_top_domain(row['acce_url'])
        if domain == '':
            continue
        if time_split not in split_time_dict:
            split_time_dict[time_split] = Counter()
        split_time_dict[time_split][domain] += 1
    return [(time, encode_domain_counter(counter)) for time, counter in split_time_dict.items()]


def save_to_csv(fileobj, uid, counter):
    writer = DictWriter(fileobj, fieldnames=['uid', 'time', 'domain_count'])
    for split_time, count in counter:
        writer.writerow({'uid': uid, 'time': split_time, 'domain_count': count})


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
            with open(csvfile, buffering=(2<<27)) as f:
                counter = domain_count_statistic(f, split_func)
            save_to_csv(outputfileobj, uid, counter)
            logging.info('[%d/%d]' % (idx + 1, n))

    logging.info('finish with time %s', str(time.time() - start))


if __name__ == '__main__':
    main()
