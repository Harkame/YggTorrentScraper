import os
import unittest

import requests

from ..yggtorrentscraper import YggTorrentScraper


class TestExtractDetails(unittest.TestCase):
    scraper = YggTorrentScraper(requests.session())

    def test_extract_details(self):
        torrent = self.scraper.extract_details(
            "https://www2.yggtorrent.pe/torrent/filmvideo/serie-tv/440445-game-of-thrones-s08e02-multi-1080p-amzn-web-dl-dd5-1-x264-ark01"
        )

        self.assertTrue(torrent.name is not None)
        self.assertTrue(torrent.uploaded_datetime is not None)
        self.assertTrue(torrent.size is not None)
        self.assertTrue(torrent.uploader is not None)

        self.assertTrue(len(torrent.keywords) > 0)

        self.assertTrue(torrent.completed > -1)
        self.assertTrue(torrent.seeders > -1)
        self.assertTrue(torrent.leechers > -1)

        self.assertTrue(torrent.url is None)

        self.assertTrue(len(torrent.files) > 0)
        self.assertTrue(len(torrent.comments) > 0)

    def test_extract_details_logged(self):
        yggtorrent_identifiant = os.environ.get("YGGTORRENT_IDENTIFIANT")
        yggtorrent_password = os.environ.get("YGGTORRENT_PASSWORD")

        self.scraper.login(yggtorrent_identifiant, yggtorrent_password)

        torrent = self.scraper.extract_details(
            "https://www2.yggtorrent.pe/torrent/filmvideo/serie-tv/440445-game-of-thrones-s08e02-multi-1080p-amzn-web-dl-dd5-1-x264-ark01"
        )

        self.assertTrue(torrent.name is not None)
        self.assertTrue(torrent.uploaded_datetime is not None)
        self.assertTrue(torrent.size is not None)
        self.assertTrue(torrent.uploader is not None)

        self.assertTrue(len(torrent.keywords) > 0)

        self.assertTrue(torrent.completed > -1)
        self.assertTrue(torrent.seeders > -1)
        self.assertTrue(torrent.leechers > -1)

        self.assertTrue(torrent.url is not None)

        self.assertTrue(len(torrent.files) > 0)
        self.assertTrue(len(torrent.comments) > 0)

    def tearDown(self):
        self.scraper.logout()
