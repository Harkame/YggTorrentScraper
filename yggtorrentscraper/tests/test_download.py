import os
import shutil
import unittest

import requests

from ..yggtorrentscraper import YggTorrentScraper


class TestDownload(unittest.TestCase):
    scraper = None
    destination_path = None

    def __init__(self, *args, **kwargs):
        super(TestDownload, self).__init__(*args, **kwargs)
        yggtorrent_identifiant = os.environ.get("YGGTORRENT_IDENTIFIANT")
        yggtorrent_password = os.environ.get("YGGTORRENT_PASSWORD")

        self.destination_path = os.path.join(
            ".", "yggtorrentscraper", "tests", "test_download"
        )

        self.scraper = YggTorrentScraper(requests.session())

        self.scraper.login(yggtorrent_identifiant, yggtorrent_password)

    def test_download_from_torrent(self):
        most_completed = self.scraper.most_completed()

        torrent = self.scraper.extract_details(most_completed[0])

        self.assertTrue(torrent.url is not None)

        file_full_path = self.scraper.download_from_torrent(
            torrent=torrent, destination_path=self.destination_path
        )

        self.assertTrue(os.path.getsize(file_full_path) > 1000)

    def test_download_from_torrent_url(self):
        file_full_path = self.scraper.download_from_torrent_url(
            torrent_url="https://www2.yggtorrent.pe/torrent/filmvideo/serie-tv/440445-game-of-thrones-s08e02-multi-1080p-amzn-web-dl-dd5-1-x264-ark01",
            destination_path=self.destination_path,
        )

        self.assertTrue(os.path.getsize(file_full_path) > 1000)

    def test_download_from_torrent_download_url(self):
        most_completed = self.scraper.most_completed()

        torrent = self.scraper.extract_details(most_completed[0])

        self.assertTrue(torrent.url is not None)

        file_full_path = self.scraper.download_from_torrent_download_url(
            torrent_url=torrent.url, destination_path=self.destination_path
        )

        self.assertTrue(os.path.getsize(file_full_path) > 1000)

    def tearDown(self):
        if os.path.exists(self.destination_path):
            shutil.rmtree(self.destination_path, ignore_errors=True)

        self.scraper.logout()
