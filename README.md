# YggTorrentScraper

[![Build Status](https://travis-ci.org/Harkame/YggTorrentScraper.svg?branch=master)](https://travis-ci.org/Harkame/YggTorrentScraper)

## Installation

``` bash

pip install yggtorrentscraper

```

OR

clone this repository and

``` bash

python setup.py install

```

### Dependencies

- [Beautiful
Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [PyYAML](https://github.com/yml/pyyml)
- [lxml](https://github.com/lxml/lxml.git)
- [Requests](https://github.com/kennethreitz/requests)

## Usage

### Initialization

``` python

import requests
from yggtorrentscraper import YggTorrentScraper

scraper = YggTorrentScraper(requests.session())

```

Session is requiered to download torrent

### Login (optionnal)

Requiered only for download torrent's file

``` python

scraper.login(identifiant='myidentifiant',
password='mypassword')

```

### Most completed

Return url's of most completed (top 100) downloaded torrents

``` python

most_completed = scraper.most_completed()

'''

https://www2.yggtorrent.ch/torrent/filmvideo/serie-tv/440445-game-of-thrones-s08e02-multi-1080p-amzn-web-dl-dd5-1-x264-ark01
https://www2.yggtorrent.ch/torrent/application/windows/316475-microsoft-toolkit-v2-6-4-activateur-office-2016---2019-windows-10
https://www2.yggtorrent.ch/torrent/filmvideo/animation/431851-asterix-le-secret-de-la-potion-magique-2018-french-1080p-hdlight-x264-ac3-toxic
https://www2.yggtorrent.ch/torrent/application/windows/330032-windows-microsoft-office-2019-build-10730-20102-activation-francais
https://www2.yggtorrent.ch/torrent/filmvideo/serie-tv/436928-game-of-thrones-s08e01-multi-1080p-amzn-web-dl-dd5-1-h264-ark01
...

'''

```

### Details

Get torrent's details

``` python
torrent = scraper.extract_details('https://www2.yggtorrent.ch/torrent/filmvideo/serie-tv/440445-game-of-thrones-s08e02-multi-1080p-amzn-web-dl-dd5-1-x264-ark01')

print(torrent)

'''

Name      : Game.of.Thrones.S08E02.MULTi.1080p.AMZN.WEB-DL.DD5.1.x264-ARK01
Url       : N/A (Not authentified)
Uploaded  : 2019-04-22 06:10:00
Size      : 1.40Go
Uploader  : Anonyme
Completed : 37157
Seeders   : 2254
Leechers  : 2

Files (1) :

Comments (15) :

'''

print(torrent.__str__(files=True, comments=True))

'''
Name      : Game.of.Thrones.S08E02.MULTi.1080p.AMZN.WEB-DL.DD5.1.x264-ARK01
Url       : N/A
Uploaded  : 2019-04-22 06:10:00
Size      : 1.40Go
Uploader  : Anonyme
Completed : 37157
Seeders   : 2254
Leechers  : 2

Files (1) :
size      :
file_name :Game.of.Thrones.S08E02.MULTi.1080p.AMZN.WEB-DL.DD5.1.x264-ARK01.mkv"}


Comments (15) :
Author : Beleg_5
Posted : 10 jours
Text   : Merci beaucoup.

Author : StephZher
Posted : 20 jours
Text   : Merci c'est cool !

...

'''

```

### Download

Download torrent's file (.torrent)

``` python

torrent = scraper.extract_details('https://www2.yggtorrent.ch/torrent/filmvideo/serie-tv/440445-game-of-thrones-s08e02-multi-1080p-amzn-web-dl-dd5-1-x264-ark01')

scraper.download_from_torrent(torrent)

'''
OR
'''

scraper.download_from_torrent_url('https://www2.yggtorrent.ch/torrent/filmvideo/serie-tv/440445-game-of-thrones-s08e02-multi-1080p-amzn-web-dl-dd5-1-x264-ark01')

```

### Logout (optionnal)

``` python

scraper.logout()

```


## Test

``` bash

pip install tox

tox

```

### Generate cover report

``` bash

pytest tests/ --cov=japscandownloader --cov-report=

```
