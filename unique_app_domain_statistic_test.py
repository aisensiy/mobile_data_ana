#!/usr/bin/env python
# encoding: utf-8

import unittest
import unique_app_domain_statistic as uads
import StringIO


class UcdsTestCase(unittest.TestCase):
    def test_this(self):
        filedata = """1998,010835,QQ,社交沟通,QQ,社交沟通,腾讯网,微信,即时聊天类,题材,即时聊天公共网站资源,weixin.qq.com,2\r
1998,010830,HTTPS,浏览,其他,-9,其他,其他,其它,其它,其它,,1\r
1998,010835,QQ,社交沟通,SAFARI浏览器,网页浏览,腾讯头像网,其他,即时聊天类,题材,即时聊天公共网站资源,qlogo.cn,7\r
1998,010835,QQLive,视频,QQLive,视频,腾讯网,信息采集,即时聊天类,题材,即时聊天公共网站资源,uu.qq.com,1\r
1998,010835,QQLive,视频,QQLive,视频,腾讯网,信息采集,即时聊天类,题材,即时聊天公共网站资源,uu.qq.com,1\r
1998,010835,QQ,社交沟通,QQ,社交沟通,腾讯头像网,其他,即时聊天类,题材,即时聊天公共网站资源,qlogo.cn,1\r
1998,010835,HTTPS,浏览,其他,-9,其他,其他,其它,其它,其它,,1\r
1998,010825,QQ,社交沟通,QQ,社交沟通,腾讯网,微信,即时聊天类,题材,即时聊天公共网站资源,weixin.qq.com,3\r
1998,010840,QQLive,视频,QQLive,视频,腾讯网,信息采集,即时聊天类,题材,即时聊天公共网站资源,uu.qq.com,3\r
1998,010835,QQ,社交沟通,SAFARI浏览器,网页浏览,腾讯头像网,其他,即时聊天类,题材,即时聊天公共网站资源,,1\r\n"""
        fileobj = StringIO.StringIO(filedata)
        targetobj = StringIO.StringIO()

        expected = """QQ,社交沟通,SAFARI浏览器,网页浏览,腾讯头像网,其他,即时聊天类,题材,即时聊天公共网站资源,qlogo.cn,7\r
QQ,社交沟通,QQ,社交沟通,腾讯网,微信,即时聊天类,题材,即时聊天公共网站资源,weixin.qq.com,5\r
QQLive,视频,QQLive,视频,腾讯网,信息采集,即时聊天类,题材,即时聊天公共网站资源,uu.qq.com,5\r
HTTPS,浏览,其他,-9,其他,其他,其它,其它,其它,,2\r
QQ,社交沟通,SAFARI浏览器,网页浏览,腾讯头像网,其他,即时聊天类,题材,即时聊天公共网站资源,,1\r
QQ,社交沟通,QQ,社交沟通,腾讯头像网,其他,即时聊天类,题材,即时聊天公共网站资源,qlogo.cn,1\r\n"""
        uads.unique_app_and_domain_statistic(fileobj, targetobj)
        self.assertEqual(expected, targetobj.getvalue())


if __name__ == '__main__':
    unittest.main()
