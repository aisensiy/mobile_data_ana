#!/usr/bin/env python
# encoding: utf-8

import unittest
import common as com


class ComTestCase(unittest.TestCase):
    def test_get_uid(self):
        self.assertEqual('0001998', com.get_uid('/anb/0001998.csv'))


if __name__ == '__main__':
    unittest.main()
