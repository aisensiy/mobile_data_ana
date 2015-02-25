#!/usr/bin/env python
# encoding: utf-8

import unittest
import gprs_count_statistic as gcs
import StringIO
from collections import Counter


class GcsTestCase(unittest.TestCase):
    def test_split_by_hour(self):
        self.assertEqual('0112', gcs.split_by_hour('20131201122222'))
        self.assertEqual('0100', gcs.split_by_hour('20131201002222'))

    def test_split_by_halfhour(self):
        self.assertEqual('0100', gcs.split_by_halfhour('20131201002222'))
        self.assertEqual('0124', gcs.split_by_halfhour('20131201122222'))
        self.assertEqual('0125', gcs.split_by_halfhour('20131201124222'))
        self.assertEqual('0147', gcs.split_by_halfhour('20131201234222'))

    def test_gprs_statistic(self):
        filedata = """31952300,2,,"4118","28495","116.353472","39.981827","HTTPS","浏览","其他","-9","20131201083010",+0000000000000149.0000,+0000000000000134.0000,+0000000000017334.0000,+0000000000090313.0000,"其他","其他","其它","其它","其它",
31952300,2,,"4118","28495","116.353472","39.981827","HTTPS","浏览","其他","-9","20131201083643",+0000000000000250.0000,+0000000000000233.0000,+0000000000030305.0000,+0000000000151108.0000,"其他","其他","其它","其它","其它",
31952300,2,,"4118","28495","116.353472","39.981827","QQLive","视频","QQLive","视频","20131201083934",+0000000000000009.0000,+0000000000000006.0000,+0000000000001632.0000,+0000000000000603.0000,"腾讯网","信息采集","即时聊天类","题材","即时聊天公共网站资源","http://monitor.uu.qq.com/analytics/upload"
31952300,2,,"4118","28495","116.353472","39.981827","QQLive","视频","QQLive","视频","20131201084036",+0000000000000007.0000,+0000000000000003.0000,+0000000000001376.0000,+0000000000000180.0000,"腾讯网","信息采集","即时聊天类","题材","即时聊天公共网站资源","http://monitor.uu.qq.com/analytics/upload"
31952300,2,,"4118","28495","116.353472","39.981827","QQLive","视频","QQLive","视频","20131201084046",+0000000000000003.0000,+0000000000000001.0000,+0000000000001144.0000,+0000000000000060.0000,"腾讯网","信息采集","即时聊天类","题材","即时聊天公共网站资源","http://monitor.uu.qq.com/analytics/upload"
31952300,2,,"4118","28495","116.353472","39.981827","QQLive","视频","QQLive","视频","20131201084052",+0000000000000007.0000,+0000000000000006.0000,+0000000000001364.0000,+0000000000000595.0000,"腾讯网","信息采集","即时聊天类","题材","即时聊天公共网站资源","http://monitor.uu.qq.com/analytics/upload"
31952300,2,,"4118","28495","116.353472","39.981827","QQ","社交沟通","QQ","社交沟通","20131201082834",+0000000000000008.0000,+0000000000000006.0000,+0000000000000807.0000,+0000000000000795.0000,"腾讯网","微信","即时聊天类","题材","即时聊天公共网站资源","http://short.weixin.qq.com/cgi-bin/micromsg-bin/getcdndns"
31952300,2,,"4118","28495","116.353472","39.981827","QQ","社交沟通","QQ","社交沟通","20131201082837",+0000000000000008.0000,+0000000000000005.0000,+0000000000000648.0000,+0000000000000830.0000,"腾讯网","微信","即时聊天类","题材","即时聊天公共网站资源","http://dns.weixin.qq.com/cgi-bin/micromsg-bin/newgetdns?uin=50974985&clientversion=352322321&scene=0&net=0"
31952300,2,,"4118","28495","116.353472","39.981827","QQ","社交沟通","QQ","社交沟通","20131201082843",+0000000000000009.0000,+0000000000000006.0000,+0000000000000688.0000,+0000000000000878.0000,"腾讯网","微信","即时聊天类","题材","即时聊天公共网站资源","http://dns.weixin.qq.com/cgi-bin/micromsg-bin/newgetdns?uin=50974985&clientversion=352322321&scene=0&net=0"
31952300,2,,"4118","28495","116.353472","39.981827","QQ","社交沟通","QQ","社交沟通","20131201083705",+0000000000000014.0000,+0000000000000020.0000,+0000000000000909.0000,+0000000000017087.0000,"腾讯头像网","其他","即时聊天类","题材","即时聊天公共网站资源","http://wx.qlogo.cn/mmhead/Q3auHgzwzM4wHV14el92fCic9TBiaqLDTibJEODJHKawQNkZGHbibmJt4Q/0"
31952300,2,,"4118","28495","116.353472","39.981827","QQ","社交沟通","QQ","社交沟通","20131201083825",+0000000000000007.0000,+0000000000000005.0000,+0000000000000731.0000,+0000000000000751.0000,"腾讯网","微信","即时聊天类","题材","即时聊天公共网站资源","http://short.weixin.qq.com/cgi-bin/micromsg-bin/getcdndns"
31952300,2,,"4118","28495","116.353472","39.981827","QQ","社交沟通","QQ","社交沟通","20131201083847",+0000000000000011.0000,+0000000000000009.0000,+0000000000000999.0000,+0000000000000987.0000,"腾讯网","微信","即时聊天类","题材","即时聊天公共网站资源","http://short.weixin.qq.com/cgi-bin/micromsg-bin/getcdndns"
31952300,2,,"4118","28495","116.353472","39.981827","QQ","社交沟通","SAFARI浏览器","网页浏览","20131201083907",+0000000000000009.0000,+0000000000000012.0000,+0000000000000759.0000,+0000000000007821.0000,"腾讯头像网","其他","即时聊天类","题材","即时聊天公共网站资源","http://q1.qlogo.cn/g?b=mqq&k=AsibS0wvKcTc24HHPoujQOA&t=1385853873&refer=mqq&s=140"
31952300,2,,"4118","28495","116.353472","39.981827","QQ","社交沟通","SAFARI浏览器","网页浏览","20131201083942",+0000000000000006.0000,+0000000000000007.0000,+0000000000000638.0000,+0000000000005209.0000,"腾讯头像网","其他","即时聊天类","题材","即时聊天公共网站资源","http://q1.qlogo.cn/g?b=mqq&k=fkmBwDFUHyzJsG7EGuVOpw&t=1380594335&refer=mqq&s=140"
31952300,2,,"4118","28495","116.353472","39.981827","QQ","社交沟通","SAFARI浏览器","网页浏览","20131201083952",+0000000000000001.0000,+0000000000000000.0000,+0000000000000415.0000,+0000000000000000.0000,"腾讯头像网","其他","即时聊天类","题材","即时聊天公共网站资源","http://q1.qlogo.cn/g?b=mqq&k=KaO9y3kqwEzDVpooLSiaOZA&t=1383370804&refer=mqq&s=140"
31952300,2,,"4118","28495","116.353472","39.981827","QQ","社交沟通","SAFARI浏览器","网页浏览","20131201083952",+0000000000000005.0000,+0000000000000005.0000,+0000000000000624.0000,+0000000000000216.0000,"腾讯头像网","其他","即时聊天类","题材","即时聊天公共网站资源","http://q4.qlogo.cn/g?b=mqq&k=n65Uj8f9gpCeEiaaOm5yUibA&t=1376003847&refer=mqq&s=140"
31952300,2,,"4118","28495","116.353472","39.981827","QQ","社交沟通","SAFARI浏览器","网页浏览","20131201083952",+0000000000000005.0000,+0000000000000009.0000,+0000000000000622.0000,+0000000000005873.0000,"腾讯头像网","其他","即时聊天类","题材","即时聊天公共网站资源","http://q4.qlogo.cn/g?b=mqq&k=pOgDldWKkhZxQU7XqVcPSA&t=1375448327&refer=mqq&s=140"
31952300,2,,"4118","28495","116.353472","39.981827","QQ","社交沟通","SAFARI浏览器","网页浏览","20131201083952",+0000000000000006.0000,+0000000000000020.0000,+0000000000000615.0000,+0000000000018282.0000,"腾讯头像网","其他","即时聊天类","题材","即时聊天公共网站资源","http://q1.qlogo.cn/g?b=mqq&k=Af9J6WTCALHwA1wibRw7QWw&t=1373608079&refer=mqq&s=140"
31952300,2,,"4118","28495","116.353472","39.981827","QQ","社交沟通","SAFARI浏览器","网页浏览","20131201083955",+0000000000000005.0000,+0000000000000005.0000,+0000000000000622.0000,+0000000000000216.0000,"腾讯头像网","其他","即时聊天类","题材","即时聊天公共网站资源","http://q2.qlogo.cn/g?b=mqq&k=M2Wv2TbvldFyjJd1Jq7gmw&t=1372566086&refer=mqq&s=140"
31952300,2,,"4118","28495","116.353472","39.981827","QQ","社交沟通","SAFARI浏览器","网页浏览","20131201083955",+0000000000000005.0000,+0000000000000008.0000,+0000000000000622.0000,+0000000000004743.0000,"腾讯头像网","其他","即时聊天类","题材","即时聊天公共网站资源","http://q2.qlogo.cn/g?b=mqq&k=RfJcBw2OQbOWF6vUeHarUQ&t=1382694255&refer=mqq&s=140"
        """
        filedata = filedata.strip()
        fileobj = StringIO.StringIO(filedata)
        self.assertEqual([('0108', 20)],
                         gcs.gprs_statistic(fileobj,
                                            gcs.split_by_hour).items())
        fileobj = StringIO.StringIO(filedata)
        self.assertEqual([('0116', 3), ('0117', 17)],
                         gcs.gprs_statistic(fileobj,
                                            gcs.split_by_halfhour).items())

    def test_save_to_csv(self):
        fileobj = StringIO.StringIO()
        counter = Counter({'0116': 3, '0117': 17})
        uid = '0001998'
        gcs.save_to_csv(fileobj, uid, counter)
        self.assertEqual('0001998,0116,3\r\n0001998,0117,17\r\n',
                         fileobj.getvalue())

    def test_get_uid(self):
        self.assertEqual('0001998', gcs.get_uid('/anb/0001998.csv'))


if __name__ == '__main__':
    unittest.main()
