"""
__init__.py main
"""
import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from .yggtorrentscraper import YggTorrentScraper, change_yggtorrent_tld, YGGTORRENT_TLD
from .torrent import Torrent, TorrentComment, TorrentFile
