import unittest

import requests

from ..yggtorrentscraper import YggTorrentScraper


class TestMostSeeded(unittest.TestCase):
    scraper = YggTorrentScraper(session=requests.session())

    def test_most_completed(self):
        most_seeded = self.scraper.most_seeded()

        self.assertEqual(len(most_seeded), 100)
