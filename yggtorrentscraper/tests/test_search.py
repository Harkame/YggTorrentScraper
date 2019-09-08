import unittest

import requests

from ..yggtorrentscraper import YggTorrentScraper


class TestResearch(unittest.TestCase):
    scraper = YggTorrentScraper(requests.session())

    def test_research(self):
        torrents_url = self.scraper.search(name="walking dead s08", category="", sub_category="",
                                           descriptions=None, files=None, uploaders=None, sort="publish_date", order="asc")

        torrent = self.scraper.extract_details(torrent_url=torrents_url[0])
