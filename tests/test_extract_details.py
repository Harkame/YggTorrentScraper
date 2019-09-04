import os
import sys
import unittest

import requests
from yggtorrentscraper import YggTorrentScraper

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../yggtorrentdownloader/')
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


class TestExtractDetails(unittest.TestCase):
    scraper = YggTorrentScraper(requests.session())

    def test_extract_details(self):
        pass
