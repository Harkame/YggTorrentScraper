import os
import unittest

import requests

from ..yggtorrentscraper import YggTorrentScraper


class TestAuthentification(unittest.TestCase):
    def setUp(self):
        self.scraper = YggTorrentScraper(requests.session())

    def test_login_success(self):
        yggtorrent_identifiant = os.environ.get("YGGTORRENT_IDENTIFIANT")
        yggtorrent_password = os.environ.get("YGGTORRENT_PASSWORD")

        self.assertTrue(yggtorrent_identifiant is not None)
        self.assertTrue(yggtorrent_password is not None)

        is_authentified = self.scraper.login(
            yggtorrent_identifiant, yggtorrent_password
        )

        self.assertTrue(is_authentified)

    def test_login_failed(self):
        is_authentified = self.scraper.login("myidentifiant", "mypassword")

        self.assertFalse(is_authentified)
