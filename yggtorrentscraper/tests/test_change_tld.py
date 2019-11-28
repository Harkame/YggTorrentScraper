import unittest

from ..yggtorrentscraper import YggTorrentScraper, YGGTORRENT_TLD, change_yggtorrent_tld


class TestChangeYggtorrentTLD(unittest.TestCase):
    current_yggtorrent_tld = None

    def test_read_tld(self):
        self.current_yggtorrent_tld = YGGTORRENT_TLD

        self.assertTrue(self.current_yggtorrent_tld == "pe")

    def test_change_yggtorrent_tld(self):
        # TODO Fix this test
        """
        change_yggtorrent_tld("newtld")

        self.assertTrue(YGGTORRENT_TLD == "newtld")
        """
        pass

    def tearDown(self):
        change_yggtorrent_tld(self.current_yggtorrent_tld)
