'''
main
'''

import logging
import sys

import requests
from yggtorrentscraper import YggTorrentScraper

logger = logging.getLogger('yggtorrentscraper')


def main(arguments):
    yggtorrentscraper = YggTorrentScraper(requests.session())

    yggtorrentscraper.login()

    most_completed = yggtorrentscraper.most_completed()

    torrent = yggtorrentscraper.extract_details(most_completed[0])

    print(torrent.__str__(files=False, comments=False))

    yggtorrentscraper.download_from_torrent(
        torrent=torrent, destination_path='./')

    yggtorrentscraper.logout()


if __name__ == '__main__':
    main(sys.argv[1:])
