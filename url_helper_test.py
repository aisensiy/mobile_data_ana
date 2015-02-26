#!/usr/bin/env python
# encoding: utf-8

import unittest
import url_helper as uh


class UhTestCase(unittest.TestCase):
    def test_get_top_domain(self):
        self.assertEqual('360.cn', uh.get_top_domain('http://md.openapi.360.cn/list/get'))
        self.assertEqual('qq.com', uh.get_top_domain('http://short.weixin.qq.com/cgi-bin/micromsg-bin/getcdndns'))
        self.assertEqual('test.com.cn', uh.get_top_domain('http://inews.test.com.cn/redisTool?type=get&key=downloadNews_158008435%2CdownloadVideo_158008435'))
        self.assertEqual('127.0.0.1', uh.get_top_domain('http://127.0.0.1/redisTool?type=get&key=downloadNews_158008435%2CdownloadVideo_158008435'))


if __name__ == '__main__':
    unittest.main()
