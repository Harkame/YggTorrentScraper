import unittest

import requests
from ..yggtorrentscraper import YggTorrentScraper


class TestMostCompleted(unittest.TestCase):
    scraper = YggTorrentScraper(session=requests.session())

    def test_most_completed(self):
        most_completed = self.scraper.most_completed()

        self.assertEqual(len(most_completed), 100)

    def tearDown(self):
        self.scraper.logout()
