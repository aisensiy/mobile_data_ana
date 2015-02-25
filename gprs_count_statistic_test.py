#!/usr/bin/env python
# encoding: utf-8

import unittest
import gprs_count_statistic as gcs


class GcsTestCase(unittest.TestCase):
    def test_split_by_hour(self):
        self.assertEqual('0112', gcs.split_by_hour('20131201122222'))
        self.assertEqual('0100', gcs.split_by_hour('20131201002222'))

    def test_split_by_halfhour(self):
        self.assertEqual('0100', gcs.split_by_halfhour('20131201002222'))
        self.assertEqual('0124', gcs.split_by_halfhour('20131201122222'))
        self.assertEqual('0125', gcs.split_by_halfhour('20131201124222'))
        self.assertEqual('0147', gcs.split_by_halfhour('20131201234222'))


if __name__ == '__main__':
    unittest.main()
