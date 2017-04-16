#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from ..main import apply_list, process_tag

__author__ = 'Hang An'


class TestAll(unittest.TestCase):

    def setUp(self):
        pass

    def test_tag(self):
        result = ['a', 'b']
        self.assertEqual(process_tag('a-b'), result)
        self.assertEqual(process_tag('a.b'), result)
        self.assertEqual(process_tag('.a.b'), result)
        self.assertEqual(process_tag('.a-b.'), result)

    def test_apply_list(self):

        def f1(l): return [x + 1 for x in l]

        def f2(l): return [x * 2 for x in l]
        data = [1, 2, 3]
        func_list = [f1, f2]
        exp = [4, 6, 8]
        self.assertEqual(apply_list(func_list, data), exp)
