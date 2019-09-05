import unittest

import requests
from yggtorrentscraper import YggTorrentScraper


class TestExtractDetails(unittest.TestCase):
    scraper = YggTorrentScraper(requests.session())

    def test_extract_details(self):
        torrent = self.scraper.extract_details('https://www2.yggtorrent.ch/torrent/filmvidéo/série-tv/3347-the+walking+dead+s05+french+web-dl+xvid-asphixias')
