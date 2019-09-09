import unittest

import requests

from ..yggtorrentscraper import YggTorrentScraper


class TestExtractDetails(unittest.TestCase):
    scraper = YggTorrentScraper(requests.session())

    def test_extract_details(self):
        torrent_url = self.scraper.most_completed()[0]

        torrent = self.scraper.extract_details(torrent_url)
