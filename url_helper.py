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


def get_domain_by_level(url, level):
    domain = get_domain(url)
    if domain:
        if ip_pn.match(domain):
            return domain
        splited_domain = domain.split('.')
        if len(splited_domain) >= 2 and \
                splited_domain[-2] in ['com', 'net', 'info', 'org', 'gov']:
            top_domain = '.'.join(splited_domain[-(level + 2):])
        else:
            top_domain = '.'.join(splited_domain[-(level + 1):])
        return top_domain
    else:
        return ''


def generate_get_right_domain(topdomain_set, seconddomain_set, blacklist):
    def get_right_domain(url):
        top_domain = get_top_domain(url)
        if top_domain in blacklist:
            return None

        second_domain = get_second_domain(url)
        if second_domain in blacklist:
            return None

        if second_domain in seconddomain_set:
            return second_domain
        elif top_domain in topdomain_set:
            return top_domain
        else:
            return None
    return get_right_domain


def get_top_domain(url):
    return get_domain_by_level(url, 1)


def get_second_domain(url):
    return get_domain_by_level(url, 2)
