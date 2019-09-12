import unittest

import requests

from ..yggtorrentscraper import YggTorrentScraper


class TestExclu(unittest.TestCase):
    scraper = YggTorrentScraper(session=requests.session())

    def test_exclus(self):
        exlus = self.scraper.exclus()
