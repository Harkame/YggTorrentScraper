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

    def setUp(self):
        if not os.path.exists(self.destination_path):
            os.makedirs(self.destination_path)

    def test_download(self):
        most_completed = self.scraper.most_completed()

        torrent = self.scraper.extract_details(most_completed[0])

        self.assertTrue(torrent.url is not None)

        self.scraper.download_from_torrent(
            torrent=torrent, destination_path=self.destination_path)

    def tearDown(self):
        if os.path.exists(self.destination_path):
            shutil.rmtree(self.destination_path, ignore_errors=True)

        self.scraper.logout()
