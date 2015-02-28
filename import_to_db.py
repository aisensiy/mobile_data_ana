#!/usr/bin/env python
# encoding: utf-8

import sqlalchemy
import pandas as pd
import logging


logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.DEBUG)

def import_app_domain_table(engine, df, tablename):
    pass


def import_location_table(engine, df, tablename):
    cols = ['uid', 'start_time', 'location']
    df.columns = cols
    import_to_db(engine, df, tablename)


def import_to_db(engine, df, tablename):
    df = pd.read_csv('38210600.reqid.csv', header=False)
    df.to_sql('test', engine)


if __name__ == '__main__':
    import sys
    import time

    start = time.time()

    filepath = sys.argv[1]
    tablename = sys.argv[2]
    tabletype = sys.argv[3]

    df = pd.read_csv(filepath, header=None)
    engine = sqlalchemy.create_engine(
        "mysql://root:000000@localhost/mobile_data_development")

    logging.info('import %s to %s', filepath, tablename)
    if tabletype == 'location':
        import_location_table(engine, df, tablename)

    logging.info('finish with time %s', str(time.time() - start))
