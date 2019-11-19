import unittest

import requests

from ..yggtorrentscraper import YggTorrentScraper, YGGTORRENT_TLD


class TestChangeYggtorrentTLD(unittest.TestCase):
    current_yggtorrent_tld = None

    def test_read_tld(self):
        self.current_yggtorrent_tld = YGGTORRENT_TLD

        self.assertTrue(self.current_yggtorrent_tld == "pe")

    def test_change_yggtorrent_tld(self):
        # YggTorrentScraper(requests.session(), yggtorrent_tld="newtld")

        # self.assertTrue(YGGTORRENT_TLD == "newtld")

        # TODO fix this test

        pass

    def tearDown(self):
        """
        Reset YGGTORRENT_TLD
        """

        YggTorrentScraper(requests.session(), self.current_yggtorrent_tld)
