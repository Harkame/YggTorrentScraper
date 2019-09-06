import unittest

import requests
from ..yggtorrentscraper import YggTorrentScraper


class TestTorrent(unittest.TestCase):
    scraper = YggTorrentScraper(requests.session())

    def test_research(self):
        torrent_url = self.scraper.search(name="walking dead s08")[0]

        torrent = self.scraper.extract_details(torrent_url)

        print(torrent.__str__(files=True, comments=True))
