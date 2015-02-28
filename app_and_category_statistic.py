#!/usr/bin/env python
# encoding: utf-8

import logging
from collections import Counter
from url_helper import generate_get_right_domain
from constants import log_header
from csv import DictWriter
from csv import DictReader
from common import get_uid
from time_helper import split_by_5_minute
from common import load_file


logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.DEBUG)

cols = ['busi_name', 'busi_type_name', 'app_name', 'app_type_name',
        'site_name', 'site_channel_name', 'cont_app_id',
        'cont_classify_id', 'cont_type_id']


def app_and_category_statistic(fileobj, get_domain_func, time_split_func):
    counter = Counter()
    reader = DictReader(fileobj, fieldnames=log_header)
    for row in reader:
        url = row['acce_url']
        minute = time_split_func(row['start_time'])

        entity = [('minute', minute),
                  ('domain', get_domain_func(url))]
        for col in cols:
            entity.append((col, row[col]))

        counter[tuple(entity)] += 1
    return counter


def save_to_csv(fileobj, uid, counter):
    fieldnames = ['uid', 'minute'] + cols + ['domain', 'count']
    writer = DictWriter(fileobj, fieldnames=fieldnames)
    for key, count in counter.items():
        key_dict = dict(key)
        key_dict['uid'] = uid
        key_dict['count'] = count
        writer.writerow(key_dict)


def main():
    import sys
    import glob
    import time
    import os
    import redis

    start = time.time()

    inputdir = sys.argv[1]
    outputfile = sys.argv[2]
    valid_user_file = sys.argv[3]
    topdomainfile = sys.argv[4]
    seconddomainfile = sys.argv[5]
    blacklistdomainfile = sys.argv[6]

    topdomain_set = set([line.strip().split(',')[0] for line in open(topdomainfile)])
    seconddomain_set = set([line.strip().split(',')[0] for line in open(seconddomainfile)])
    blacklistdomain_set = set([line.strip().split(',')[0] for line in open(blacklistdomainfile)])

    valid_users = set([line.strip() for line in open(valid_user_file)])
    split_func = split_by_5_minute
    get_domain_func = generate_get_right_domain(topdomain_set, seconddomain_set, blacklistdomain_set)

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    csvfiles = glob.glob(os.path.join(inputdir, '*', '*.csv'))
    n = len(csvfiles)
    outputobj = open(outputfile, 'w')

    for idx, csvfile in enumerate(csvfiles):
        uid = get_uid(csvfile)
        if uid not in valid_users:
            continue
        f = load_file(r, csvfile)
        counter = app_and_category_statistic(f, get_domain_func, split_func)
        f.close()
        save_to_csv(outputobj, uid, counter)
        logging.info('[%d/%d]' % (idx + 1, n))

    logging.info('finish with time %s', str(time.time() - start))
    outputobj.close()


if __name__ == '__main__':
    main()
