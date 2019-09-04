
import requests
from yggtorrentscraper import YggTorrentScraper

session = requests.session()

scraper = YggTorrentScraper(session=session)

scraper.login('a', 'b')

research = scraper.search(name='walking dead s08')

for torrent_url in research:
    print(torrent_url)

torrent = scraper.extract_details(research[1])

print(torrent.__str__(comments=True))
