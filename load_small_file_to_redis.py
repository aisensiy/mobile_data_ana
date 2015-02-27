#!/usr/bin/env python
# encoding: utf-8

import redis
from common import get_uid
import logging


logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.DEBUG)


def load_file_to_redis(redis_server, filepath, fileobj):
    redis_server.set(filepath, fileobj.read())


if __name__ == '__main__':
    import glob
    import sys
    import time
    import os

    start = time.time()

    inputdir = sys.argv[1]
    small_uids_file = sys.argv[2]

    small_uids = set([line.strip() for line in open(small_uids_file)])
    csvfiles = glob.glob(os.path.join(inputdir, '*', '*.csv'))
    n = len(csvfiles)

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for idx, csvfile in enumerate(csvfiles):
        uid = get_uid(csvfile)
        if uid not in small_uids:
            continue
        with open(csvfile, buffering=(2 << 22)) as f:
            load_file_to_redis(r, csvfile, f)
        logging.info('[%d/%d]' % (idx + 1, n))

    logging.info('finish with time %s', str(time.time() - start))
