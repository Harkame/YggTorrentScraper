import os
import unittest

import requests

from ..yggtorrentscraper import YggTorrentScraper


class TestTorrent(unittest.TestCase):
    scraper = YggTorrentScraper(requests.session())

    def test_str(self):
        torrent_url = self.scraper.most_completed()[0]

        torrent = self.scraper.extract_details(torrent_url)

        torrent.__str__(files=True, comments=True)

    def test_str_logged(self):
        yggtorrent_identifiant = os.environ.get("YGGTORRENT_IDENTIFIANT")
        yggtorrent_password = os.environ.get("YGGTORRENT_PASSWORD")

        self.scraper.login(yggtorrent_identifiant, yggtorrent_password)

        torrent_url = self.scraper.most_completed()[0]

        torrent = self.scraper.extract_details(torrent_url)

        torrent.__str__(files=True, comments=True)

    def tearDown(self):
        self.scraper.logout()
