#!/usr/bin/env python
# encoding: utf-8

from constants import log_header
from csv import DictReader
import datetime
from url_helper import get_top_domain

max_request_delta = 60


def prepare_user_log(fileobj):
    reader = DictReader(fileobj, fieldnames=log_header)
    rows = []

    for row in reader:
        if row['acce_url']:
            row['top_domain'] = get_top_domain(row['acce_url'])
        else:
            row['top_domain'] = ''
        rows.append(row)

    rows.sort(key=lambda x: (x['start_time'], x['top_domain']))
    return map(lambda x: {'start_time': x['start_time'], 'top_domain': x['top_domain']}, rows)


def string_to_datetime(string):
    return datetime.datetime.strptime(string, '%Y%m%d%H%M%S')


def create_user_requests(rows, max_request_delta=max_request_delta):
    requests = []

    start_request_datetime = None
    last_datetime = None
    last_top_domain = None
    cur_request = []

    for row in rows:
        cur_datetime = string_to_datetime(row['start_time'])
        top_domain = row['top_domain']
        if last_datetime:
            delta_seconds = int((cur_datetime - last_datetime).total_seconds())
        else: # If first line
            delta_seconds = 0
            start_request_datetime = cur_datetime

        if last_datetime is not None and \
            (delta_seconds > max_request_delta or
                top_domain != last_top_domain):
            requests.append((start_request_datetime, last_datetime, cur_request))
            cur_request = []
            start_request_datetime = cur_datetime

        cur_request.append(row)
        last_datetime = cur_datetime
        last_top_domain = top_domain

    requests.append((start_request_datetime, last_datetime, cur_request))
    return requests


def print_user_request(requests):
    for start, end, request_array in requests:
        print '%s -- %s domain: %s req: [%d]' % (start.strftime('%d %H:%M'),
                                                 end.strftime('%d %H:%M'),
                                                 request_array[0]['top_domain'], len(request_array))


if __name__ == '__main__':
    import sys
    filepath = sys.argv[1]
    with open(filepath) as f:
        rows = prepare_user_log(f)
        print_user_request(create_user_requests(rows))
