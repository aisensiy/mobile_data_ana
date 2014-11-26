#!/usr/bin/env python
# encoding: utf-8

log_header = ['user_id', 'access_mode_id', 'logic_area_name', 'lac',
              'ci', 'longitude', 'latitude', 'busi_name',
              'busi_type_name', 'app_name', 'app_type_name', 'start_time',
              'up_pack', 'down_pack', 'up_flow', 'down_flow',
              'site_name', 'site_channel_name', 'cont_app_id',
              'cont_classify_id', 'cont_type_id', 'acce_url']

clean_log_header = log_header[:] + ['location', 'day', 'hour']

noinvalid_clean_log_header = clean_log_header[:] + ['duration', 'distance', 'speed']

call_headers = ['user_id', 'target_id', 'start_time',
                'end_time', 'roam', 'basename',
                'longitude', 'latitude']

locallist_headers = ['user_id', 'locations', 'location_size', 'date']

location_related_header = [
    'user_id', 'lac', 'longitude', 'latitude', 'start_time'
]

merged_location_related_header = [
    'user_id', 'lac', 'longitude', 'latitude', 'start_time', 'type'
]

loc_app_cols = [
    'user_id', 'lac', 'longitude', 'latitude', 'busi_name', 'start_time'
]

loc_app_sid_cols = [
    'user_id', 'lac', 'longitude', 'latitude', 'busi_name', 'start_time', 'sid'
]

db = {}
db['dev'] = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '000000',
    'port': 3306,
    'charset': 'utf8',
    'db': 'chinamobile'
}
db['demo'] = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '000000',
    'port': 3306,
    'charset': 'utf8',
    'db': 'chinamobile_for_demo'
}
db['demo_noinvalid'] = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '000000',
    'port': 3306,
    'charset': 'utf8',
    'db': 'chinamobile_for_demo_noinvalid'
}
db['production'] = {
    'host': '162.105.19.244',
    'user': 'beijingmobile',
    'passwd': 'KVision.im',
    'port': 3306,
    'charset': 'utf8',
    'db': 'beijingmobile_sample0x'
}

BAIDU_MAP_AK = '5feeb91553679e8baa2c5439e5fc0e75'
