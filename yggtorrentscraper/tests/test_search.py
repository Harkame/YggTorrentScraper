import unittest

import requests

from ..yggtorrentscraper import YggTorrentScraper


class TestResearch(unittest.TestCase):
    scraper = YggTorrentScraper(requests.session())

    def test_search(self):
        torrents_url = self.scraper.search(name="walking dead s08", category="", sub_category="",
                                           descriptions=None, files='mkv', uploaders={'Team_QTZ'}, sort="publish_date", order="asc")

        # torrent = self.scraper.extract_details(torrent_url=torrents_url[0])
    '''
    def test_search_uploaders(self):
        torrents_url = self.scraper.search(
            name="walking dead", uploaders="Team_QTZ")

        torrent = self.scraper.extract_details(torrents_url[0])

        self.assertTrue(torrent.uploader.lower() == 'Team_QTZ'.lower())
    '''
    '''
    def test_search_name(self):
        torrents_url = self.scraper.search(name="walking dead")

    def test_search_category(self):
        torrents_url = self.scraper.search(name="walking dead")

    def test_search_sub_category(self):
        torrents_url = self.scraper.search(name="walking dead")

    def test_search_descriptions(self):
        torrents_url = self.scraper.search(name="walking dead")


    def test_search_sort(self):
        torrents_url = self.scraper.search(name="walking dead")
    '''

    def test_search_multiple_page(self):
        torrents_url = self.scraper.search(name="walking dead")

        self.assertTrue(len(torrents_url) > 200)
