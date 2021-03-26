# -*- coding: utf-8 -*-

import unittest
from tmp_generate_file import TestBrandRegTool
from HTMLTestRunner import HTMLTestRunner
import configparser
import time

if __name__ == '__main__':

    config_file = "utest_online_data_update.cfg"
    suite = unittest.TestSuite()
    config = configparser.ConfigParser()
    config.read(config_file,encoding="utf-8")
    sec = config.sections()
    for sec_item in sec:
        suite.addTest(TestBrandRegTool('test_clean_brand_' + sec_item))

    cur_time = time.strftime("%Y-%m-%d_%H")
    html_file = 'utest_online_html_report/%s.html' % cur_time
    with open(html_file, 'wb') as f:
        runner = HTMLTestRunner(stream=f,
                                title='抖音品牌清洗 单元测试报告',
                                description=cur_time + '测试报告',
                                verbosity=2
                                )
        runner.run(suite)