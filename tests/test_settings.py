'''
import os
import sys
import unittest

import settings

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../yggtorrentscraper/')
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


class SettingsTest(unittest.TestCase):
    def test_settings_init_arguments(self):
        settings.init_arguments('')

    def test_settings_init_config(self):
        # settings.init_config()
        pass
'''
