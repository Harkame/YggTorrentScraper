import unittest

from ..yggtorrentscraper import (
    YggTorrentScraper,
    set_yggtorrent_tld,
    get_yggtorrent_tld,
)


class TestChangeYggtorrentTLD(unittest.TestCase):
    current_yggtorrent_tld = get_yggtorrent_tld()

    def test_read_tld(self):
        self.current_yggtorrent_tld = get_yggtorrent_tld()

        self.assertTrue(self.current_yggtorrent_tld == "ws")

    def test_set_yggtorrent_tld(self):

        set_yggtorrent_tld("newtld")

        self.assertTrue(get_yggtorrent_tld() == "newtld")
        pass

    def tearDown(self):
        set_yggtorrent_tld(self.current_yggtorrent_tld)
