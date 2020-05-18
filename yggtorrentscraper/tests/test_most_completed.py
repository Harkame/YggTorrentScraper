import unittest

import requests
import cloudscraper
from ..yggtorrentscraper import YggTorrentScraper


class TestMostCompleted(unittest.TestCase):
    self.scraper = YggTorrentScraper(cloudscraper.create_scraper())

    def test_most_completed(self):
        most_completed = self.scraper.most_completed()

        self.assertEqual(len(most_completed), 100)

    def tearDown(self):
        self.scraper.logout()
