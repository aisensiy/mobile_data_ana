#!/usr/bin/env python
# encoding: utf-8

import re

url_pn = re.compile('^\S+//([^\/]+)/')
ip_pn = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')


def get_domain(url):
    url_match = url_pn.match(url)
    if url_match:
        return url_match.group(1)
    else:
        return ''


def get_top_domain(url):
    domain = get_domain(url)
    if domain:
        if ip_pn.match(domain):
            return domain
        splited_domain = domain.split('.')
        if len(splited_domain) >= 2 and \
                splited_domain[-2] in ['com', 'net', 'info']:
            top_domain = '.'.join(splited_domain[-3:])
        else:
            top_domain = '.'.join(splited_domain[-2:])
        return top_domain
    else:
        return ''


def get_second_domain(url):
    domain = get_domain(url)
    if domain:
        if ip_pn.match(domain):
            return domain
        splited_domain = domain.split('.')
        if len(splited_domain) >= 2 and \
                splited_domain[-2] in ['com', 'net', 'info']:
            level_domain = '.'.join(splited_domain[-4:])
        else:
            level_domain = '.'.join(splited_domain[-3:])
        return level_domain
    else:
        return ''
