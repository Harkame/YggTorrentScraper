import unittest

import requests
from yggtorrentscraper import YggTorrentScraper


class TestConnection(unittest.TestCase):
    scraper = YggTorrentScraper(requests.session())

    def test_login_success(self):
        is_authentified = self.scraper.login('myidentifiant', 'mypassword')

        self.assertFalse(is_authentified)

    def test_login_failed(self):
        is_authentified = self.scraper.login('myidentifiant', 'mypassword')

        self.assertFalse(is_authentified)

    def test_logout(self):
        self.scraper.logout()
