import unittest

import requests
from ..yggtorrentscraper import YggTorrentScraper


class TestDownload(unittest.TestCase):
    scraper = YggTorrentScraper(requests.session())

    def test_download(self):
        pass
