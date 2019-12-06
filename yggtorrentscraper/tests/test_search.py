import unittest

import requests

from ..yggtorrentscraper import YggTorrentScraper


class TestResearch(unittest.TestCase):
    scraper = YggTorrentScraper(requests.session())

    torrent_name = "walking dead s09"
    torrent_uploader = "brandit"

    torrent_name_2 = "blue oyster cult"

    def test_search_by_name(self):
        torrents_url = self.scraper.search({"name": self.torrent_name})

        torrent = self.scraper.extract_details(torrents_url[0])

        splited_searched_name = self.torrent_name.split(" ")

        for word in splited_searched_name:
            self.assertTrue(word.lower() in torrent.name.lower())

    def test_search_by_uploader(self):
        torrents_url = self.scraper.search(
            {"name": self.torrent_name, "uploader": self.torrent_uploader}
        )

        for torrent_url in torrents_url:
            torrent = self.scraper.extract_details(torrent_url)

            self.assertTrue(torrent.uploader.lower() == self.torrent_uploader.lower())

    def test_search_sort_completed_asc(self):
        torrents_url = self.scraper.search(
            {"name": "blue oyster cult", "sort": "completed", "order": "asc"}
        )

        torrent_old = None

        for torrent_url in torrents_url:
            torrent = self.scraper.extract_details(torrent_url)

            if torrent_old is not None:
                self.assertTrue(torrent_old.completed <= torrent.completed)
                torrent_old = torrent

    def test_search_sort_completed_desc(self):
        torrents_url = self.scraper.search(
            {"name": "blue oyster cult", "sort": "completed", "order": "desc"}
        )

        torrent_old = None

        for torrent_url in torrents_url:
            torrent = self.scraper.extract_details(torrent_url)

            if torrent_old is not None:
                self.assertTrue(torrent_old.completed >= torrent.completed)
                torrent_old = torrent

    def test_search_multiple_page(self):
        torrents_url = self.scraper.search({"name": "walking dead"})

        self.assertTrue(len(torrents_url) > 200)

    def tearDown(self):
        self.scraper.logout()
