#!/usr/bin/env python
# encoding: utf-8

import sqlalchemy
from sqlalchemy import MetaData, String, Integer, Table, Column, Float, DateTime
import pandas as pd
import logging


logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.DEBUG)


def create_phonecall_table(tablename, engine):
    meta = MetaData(bind=engine)
    Table(tablename, meta,
          Column('id', Integer, primary_key=True, autoincrement=True),
          Column('uid', String(16), nullable=False),
          Column('start_time', DateTime),
          Column('end_time', DateTime),
          Column('location', String(18)),
          mysql_charset='utf8')
    meta.create_all(engine)


def import_phonecall_table(engine, filepath, tablename, chunksize=10000):
    cols = ['uid', 'start_time', 'end_time', 'lng', 'lat']
    df = pd.read_csv(filepath,
                     names=cols,
                     dtype={'uid': str, 'lng': str, 'lat': str},
                     chunksize=chunksize)

    for dataframe in df:
        dataframe['location'] = dataframe.lng + ' ' + dataframe.lat
        del dataframe['lng']
        del dataframe['lat']
        import_to_db(engine, dataframe, tablename)
        logging.info('a chunk')


def create_user_table(tablename, engine):
    meta = MetaData(bind=engine)
    Table(tablename, meta,
          Column('id', Integer, primary_key=True, autoincrement=True),
          Column('uid', String(16), nullable=False),
          Column('gender', String(4)),
          Column('age', Integer),
          Column('education_name', String(255)),
          Column('user_opentime', String(255)),
          Column('brand_name', String(255)),
          Column('call_duration_m', Integer),
          Column('gprs_flow', Float),
          Column('call_fee', Float),
          Column('gprs_fee', Float),
          Column('databusiness_fee', Float),
          Column('brand_chn', String(255)),
          Column('model_chn', String(255)),
          Column('screensize', Float),
          Column('operation_sys', String(255)),
          Column('terminal_price', Float),
          Column('dept_country_name', String(255)),
          Column('dept_name', String(255)),
          mysql_charset='utf8')
    meta.create_all(engine)


def import_user_table(engine, filepath, tablename, chunksize=10000):
    cols = ['uid', 'gender', 'age', 'education_name',
            'user_opentime', 'brand_name', 'call_duration_m',
            'gprs_flow', 'call_fee', 'gprs_fee', 'databusiness_fee',
            'brand_chn', 'model_chn', 'screensize', 'operation_sys',
            'terminal_price', 'dept_country_name', 'dept_name']
    df = pd.read_csv(filepath,
                     names=cols,
                     dtype={'uid': str, 'user_opentime': str},
                     chunksize=chunksize)

    for dataframe in df:
        import_to_db(engine, dataframe, tablename)
        logging.info('a chunk')


def import_app_domain_table(engine, filepath, tablename, chunksize=10000):
    cols = ['busi_name', 'busi_type_name', 'app_name', 'app_type_name',
            'site_name', 'site_channel_name', 'cont_app_id',
            'cont_classify_id', 'cont_type_id']
    cols = ['uid', 'minute'] + cols + ['domain', 'count']
    df = pd.read_csv(filepath,
                     names=cols,
                     dtype={'uid': str, 'minute': str},
                     chunksize=chunksize)

    for dataframe in df:
        dataframe['day'] = dataframe.minute.map(lambda x: x[:2])
        import_to_db(engine, dataframe, tablename)
        logging.info('a chunk')


def create_app_domain_table(tablename, engine):
    meta = MetaData(bind=engine)
    Table(tablename, meta,
          Column('id', Integer, primary_key=True, autoincrement=True),
          Column('uid', String(16), nullable=False),
          Column('day', String(2)),
          Column('minute', String(6)),
          Column('busi_name', String(255)),
          Column('busi_type_name', String(255)),
          Column('app_name', String(255)),
          Column('app_type_name', String(255)),
          Column('site_name', String(255)),
          Column('site_channel_name', String(255)),
          Column('cont_app_id', String(255)),
          Column('cont_classify_id', String(255)),
          Column('cont_type_id', String(255)),
          Column('domain', String(255)),
          Column('count', Integer),
          mysql_charset='utf8')
    meta.create_all(engine)


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
        # for col in cols:
        #     dataframe[col] = dataframe[col].str.decode('utf8')
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
    engine = sqlalchemy.create_engine(dbstring, encoding='utf-8')

    logging.info('import %s to %s', filepath, tablename)
    if tabletype == 'location':
        create_location_table(tablename, engine)
        import_location_table(engine, filepath, tablename)
    elif tabletype == 'gprs_hour_count':
        create_grps_hour_stat_table(tablename, engine)
        import_gprs_hour_stat_table(engine, filepath, tablename)
    elif tabletype == 'app_domain':
        create_app_domain_table(tablename, engine)
        import_app_domain_table(engine, filepath, tablename)
    elif tabletype == 'user':
        create_user_table(tablename, engine)
        import_user_table(engine, filepath, tablename)
    elif tabletype == 'call':
        create_phonecall_table(tablename, engine)
        import_phonecall_table(engine, filepath, tablename)

    logging.info('finish with time %s', str(time.time() - start))
