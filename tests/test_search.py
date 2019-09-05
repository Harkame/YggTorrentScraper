
import unittest

import requests
from yggtorrentscraper import YggTorrentScraper


class TestResearch(unittest.TestCase):
    scraper = YggTorrentScraper(requests.session())

    def test_research(self):
        torrent_url = self.scraper.search(name='walking dead s08')
