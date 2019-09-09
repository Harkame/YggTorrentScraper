import unittest

import requests

from ..yggtorrentscraper import YggTorrentScraper


class TestTorrent(unittest.TestCase):
    scraper = YggTorrentScraper(requests.session())

    def test_str(self):
        torrent_url = self.scraper.most_completed()[0]

        torrent = self.scraper.extract_details(torrent_url)

        torrent.__str__(files=True, comments=True)
