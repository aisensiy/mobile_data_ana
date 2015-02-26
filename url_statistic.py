#!/usr/bin/env python
# encoding: utf-8

"""
统计一级、二级域名的分布
"""

import logging
from collections import Counter
from url_helper import get_top_domain
from url_helper import get_second_domain
from csv import DictWriter
from common import get_uid


logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.DEBUG)


def get_url(line):
    return line.rsplit(',', 1)[-1]


def domain_statistic(fileobj):
    top_counter = Counter()
    second_counter = Counter()
    for line in fileobj:
        url = get_url(line)
        top_counter[get_top_domain(url)] += 1
        second_counter[get_second_domain(url)] += 1
    return top_counter.items(), second_counter.items()


def save_to_csv(fileobj, uid, counter):
    writer = DictWriter(fileobj, fieldnames=['uid', 'domain', 'count'])
    for domain, count in counter:
        writer.writerow({'uid': uid, 'domain': domain, 'count': count})


def main():
    import sys
    import glob
    import time
    import os

    start = time.time()

    inputdir = sys.argv[1]
    topdomainfile = sys.argv[2]
    seconddomainfile = sys.argv[3]

    csvfiles = glob.glob(os.path.join(inputdir, '*', '*.csv'))
    n = len(csvfiles)

    topdomainobj = open(topdomainfile, 'w')
    seconddomainobj = open(seconddomainfile, 'w')
    for idx, csvfile in enumerate(csvfiles):
        uid = get_uid(csvfile)
        with open(csvfile, buffering=(2 << 27)) as f:
            topcounter, secondcounter = domain_statistic(f)
        save_to_csv(topdomainobj, uid, topcounter)
        save_to_csv(seconddomainobj, uid, secondcounter)
        logging.info('[%d/%d]' % (idx + 1, n))

    logging.info('finish with time %s', str(time.time() - start))
    topdomainobj.close()
    seconddomainobj.close()


if __name__ == '__main__':
    main()
