import unittest

import yggtorrentscraper.helpers


class ConfigTest(unittest.TestCase):
    def test_login(self):
        yggtorrent_token = helpers.login('identifiant', 'password')

    def test_logout(self):
        yggtorrent_token = helpers.login('identifiant', 'password')

        helpers.logout(yggtorrent_token)
