"""
__init__.py main
"""

from .yggtorrentscraper import (
    YggTorrentScraper,
    set_yggtorrent_tld,
    get_yggtorrent_tld,
)
from .torrent import Torrent, TorrentComment, TorrentFile
from .categories import categories
