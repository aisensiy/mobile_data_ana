#!/usr/bin/env python
# encoding: utf-8

"""
sample by last two numbers of user_id
"""

import shutil
import os
import glob
import logging

logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.INFO)


def create_dir_if_not_exists(dst_dir):
    if not os.path.isdir(dst_dir):
        os.mkdir(dst_dir)


def copy_dir(src_dir, dst_dir):
    create_dir_if_not_exists(dst_dir)
    csv_files = glob.glob(os.path.join(src_dir, '*.csv'))
    for idx, csv_file in enumerate(csv_files):
        if idx % 50 == 0 and idx != 0:
            logging.info('Already %d files from %s => %s',
                         idx, src_dir, dst_dir)
        shutil.copy(csv_file, dst_dir)


def copy_dir_by_sys(src_dir, dst_dir):
    os.system("cp -rf %s %s" % (src_dir, dst_dir))


def main(src_dir, dst_dir, start, end):
    create_dir_if_not_exists(dst_dir)
    for subdir in ["%02d" % num for num in range(start, end + 1)]:
        from_dir = os.path.join(src_dir, subdir)
        to_dir = os.path.join(dst_dir, subdir)
        logging.info("copy %s to %s", from_dir, to_dir)
        copy_dir_by_sys(from_dir, to_dir)


if __name__ == '__main__':
    import sys
    src_dir = sys.argv[1]
    dst_dir = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    main(src_dir, dst_dir, start, end)
