"""
__init__.py main
"""
import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from .yggtorrentscraper import (
    YggTorrentScraper,
    set_yggtorrent_tld,
    get_yggtorrent_tld,
)
from .torrent import Torrent, TorrentComment, TorrentFile
