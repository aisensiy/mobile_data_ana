#!/usr/bin/env python
# encoding: utf-8

import sqlalchemy
from sqlalchemy import MetaData, String, Integer, Table, Column
import pandas as pd
import logging


logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.DEBUG)


def import_app_domain_table(engine, df, tablename):
    pass


def import_gprs_hour_stat_table(engine, filepath, tablename, chunksize=10000):
    cols = ['uid', 'hour', 'count']
    df = pd.read_csv(filepath,
                     names=cols,
                     dtype={'uid': str, 'hour': str},
                     chunksize=chunksize)

    for dataframe in df:
        dataframe['day'] = dataframe.hour.map(lambda x: x[:2])
        dataframe['hour'] = dataframe.hour.map(lambda x: x[-2:])
        import_to_db(engine, dataframe, tablename)
        logging.info('a chunk')


def create_grps_hour_stat_table(tablename, engine):
    meta = MetaData(bind=engine)
    Table(tablename, meta,
          Column('id', Integer, primary_key=True, autoincrement=True),
          Column('uid', String(16), nullable=False),
          Column('day', String(2)),
          Column('hour', String(2)),
          Column('count', Integer))
    meta.create_all(engine)


def create_location_table(tablename, engine):
    meta = MetaData(bind=engine)
    Table(tablename, meta,
          Column('id', Integer, primary_key=True, autoincrement=True),
          Column('uid', String(16), nullable=False),
          Column('start_time', String(14)),
          Column('location', String(18)))
    meta.create_all(engine)


def import_location_table(engine, filepath, tablename, chunksize=10000):
    cols = ['uid', 'start_time', 'location']
    df = pd.read_csv(filepath,
                     names=cols,
                     dtype={'uid': str, 'start_time': str},
                     chunksize=chunksize)
    for dataframe in df:
        import_to_db(engine, dataframe, tablename)
        logging.info('a chunk')


def import_to_db(engine, df, tablename):
    df.to_sql(tablename, engine, index=False,
              if_exists='append', chunksize=1000)


if __name__ == '__main__':
    import sys
    import time

    start = time.time()

    filepath = sys.argv[1]
    tablename = sys.argv[2]
    tabletype = sys.argv[3]
    dbstring = sys.argv[4]

    # "mysql://root:000000@localhost/mobile_data_development"
    engine = sqlalchemy.create_engine(dbstring)

    logging.info('import %s to %s', filepath, tablename)
    if tabletype == 'location':
        create_location_table(tablename, engine)
        import_location_table(engine, filepath, tablename)
    elif tabletype == 'gprs_hour_count':
        create_grps_hour_stat_table(tablename, engine)
        import_gprs_hour_stat_table(engine, filepath, tablename)

    logging.info('finish with time %s', str(time.time() - start))
