#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
file: coverageTest.py
created time : 2021/02/25
last edit time : 2021/04/18
author : Zhenyu Wei 
version : 1.0
contact : zhenyuwei99@gmail.com
copyright : (C)Copyright 2021-2021, Zhenyu Wei and Southeast University
'''

import pytest, os
cur_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
test_dir = os.path.join(cur_dir, 'tests')

if __name__ == '__main__':
    pytest.main(['-sv', '-r P', test_dir])