import unittest

import requests

from ..yggtorrentscraper import YggTorrentScraper


class TestResearch(unittest.TestCase):
    scraper = YggTorrentScraper(requests.session())

    torrent_name = "walking dead s09"
    torrent_uploaders = ["brandit", "mrchris44"]

    torrent_name_2 = "blue oyster cult"

    def test_search(self):
        torrents_url = self.scraper.search(
            name="walking dead s08",
            category="",
            sub_category="",
            descriptions=None,
            files="mkv",
            sort="publish_date",
            order="asc",
        )

        # torrent = self.scraper.extract_details(torrent_url=torrents_url[0])

    def test_search_name(self):
        torrents_url = self.scraper.search(name=self.torrent_name)

        torrent = self.scraper.extract_details(torrents_url[0])

        splited_searched_name = self.torrent_name.split(" ")

        for word in splited_searched_name:
            self.assertTrue(word.lower() in torrent.name.lower())

    def test_search_uploader(self):
        torrents_url = self.scraper.search(
            name=self.torrent_name, uploaders={self.torrent_uploaders[0]}
        )

        for torrent_url in torrents_url:
            torrent = self.scraper.extract_details(torrent_url)

            self.assertTrue(
                torrent.uploader.lower() == self.torrent_uploaders[0].lower()
            )

    """
    def test_search_sort_publish_date_asc(self):
        torrents_url = self.scraper.search(
            name="blue oyster cult", sort="publish_date", order="asc"
        )

    def test_search_sort_publish_date_desc(self):
        torrents_url = self.scraper.search(
            name="blue oyster cult", sort="completed", order="desc"
        )

    def test_search_sort_size_asc(self):
        torrents_url = self.scraper.search(
            name="blue oyster cult", sort="leech", order="desc"
        )

    def test_search_sort_size_desc(self):
        torrents_url = self.scraper.search(
            name="blue oyster cult", sort="leech", order="desc"
        )

    def test_search_sort_completed_asc(self):
        torrents_url = self.scraper.search(
            name="blue oyster cult", sort="completed", order="asc"
        )

        torrent_old = None

        for torrent_url in torrents_url:
            torrent = self.scraper.extract_details(torrent_url)

            if torrent_old is not None:
                self.assertTrue(torrent_old.completed <= torrent.completed)

            torrent_old = torrent

    def test_search_sort_completed_desc(self):
        torrents_url = self.scraper.search(
            name="blue oyster cult", sort="completed", order="desc"
        )

        torrent_old = None

        for torrent_url in torrents_url:
            torrent = self.scraper.extract_details(torrent_url)

            if torrent_old is not None:
                self.assertTrue(torrent_old.completed >= torrent.completed)

            torrent_old = torrent

    def test_search_sort_seed_asc(self):
        torrents_url = self.scraper.search(
            name="blue oyster cult", sort="seed", order="asc"
        )

        torrent_old = None

        for torrent_url in torrents_url:
            torrent = self.scraper.extract_details(torrent_url)

            if torrent_old is not None:
                self.assertTrue(torrent_old.seeders <= torrent.seeders)

            torrent_old = torrent

    def test_search_sort_seed_desc(self):
        torrents_url = self.scraper.search(
            name="blue oyster cult", sort="seed", order="desc"
        )

        torrent_old = None

        for torrent_url in torrents_url:
            torrent = self.scraper.extract_details(torrent_url)

            if torrent_old is not None:
                self.assertTrue(torrent_old.seeders >= torrent.seeders)

            torrent_old = torrent

    def test_search_sort_leech_asc(self):
        torrents_url = self.scraper.search(
            name="blue oyster cult", sort="leech", order="asc"
        )

        torrent_old = None

        for torrent_url in torrents_url:
            torrent = self.scraper.extract_details(torrent_url)

            if torrent_old is not None:
                self.assertTrue(torrent_old.leechers <= torrent.leechers)

            torrent_old = torrent

    def test_search_sort_leech_desc(self):
        torrents_url = self.scraper.search(
            name="blue oyster cult", sort="leech", order="desc"
        )

        torrent_old = None

        for torrent_url in torrents_url:
            torrent = self.scraper.extract_details(torrent_url)

            if torrent_old is not None:
                self.assertTrue(torrent_old.leechers >= torrent.leechers)

            torrent_old = torrent

    """

    def test_search_multiple_page(self):
        torrents_url = self.scraper.search(name="walking dead")

        self.assertTrue(len(torrents_url) > 200)
