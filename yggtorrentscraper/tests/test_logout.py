import os
import unittest

import requests

from ..yggtorrentscraper import YggTorrentScraper


class TestLogout(unittest.TestCase):
    def setUp(self):
        self.scraper = YggTorrentScraper(requests.session())

    def test_logout_success(self):
        yggtorrent_identifiant = os.environ.get("YGGTORRENT_IDENTIFIANT")
        yggtorrent_password = os.environ.get("YGGTORRENT_PASSWORD")

        self.assertTrue(self.scraper.login(yggtorrent_identifiant, yggtorrent_password))

        self.assertTrue(self.scraper.logout())

    def test_logout_failed(self):
        self.scraper.login("myidentifiant", "mypassword")

        self.assertFalse(self.scraper.logout())

    def tearDown(self):
        self.scraper.logout()
