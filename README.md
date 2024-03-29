# YggTorrentScraper

[![PyPI version](https://badge.fury.io/py/yggtorrentscraper.svg)](https://badge.fury.io/py/yggtorrentscraper)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2d860dc88dfa467eb07105f559ba352a)](https://www.codacy.com/app/Harkame/YggTorrentScraper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Harkame/YggTorrentScraper&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/341218ef79de77052e43/maintainability)](https://codeclimate.com/github/Harkame/YggTorrentScraper/maintainability)
[![Build Status](https://travis-ci.org/Harkame/YggTorrentScraper.svg?branch=master)](https://travis-ci.org/Harkame/YggTorrentScraper)
[![codecov](https://codecov.io/gh/Harkame/YggTorrentScraper/branch/master/graph/badge.svg)](https://codecov.io/gh/Harkame/YggTorrentScraper)

## Installation

``` bash

pip install yggtorrentscraper

```

OR

clone this repository and

``` bash

pip install -r requirements.txt

python setup.py install

```

### Dependencies

-   [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
-   [lxml](https://github.com/lxml/lxml.git)
-   [requests](https://github.com/psf/requests.git)
-   [Google Chrome](https://www.google.com/chrome/)
-   [ChromeDriver](https://chromedriver.chromium.org)
-   [undetected_chromedriver](https://pypi.org/project/undetected-chromedriver/)

## Usage

### Initialization

Actual cloudflare bypassers like https://github.com/VeNoMouS/cloudscraper seem to have some difficulties for now. Only Selenium version is working.


``` python

import requests
from yggtorrentscraper import YggTorrentScraper

session = requests.session()

scraper = YggTorrentScraper(session)

```

Selenium version

``` python
from yggtorrentscraper import YggTorrentScraperSelenium
from selenium import webdriver
import undetected_chromedriver.v2 as uc

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = uc.Chrome("D:\chromedriver.exe", options=options)

scraper = YggTorrentScraperSelenium(driver=driver)

#OR

scraper = YggTorrentScraperSelenium(driver_path="D:\chromedriver.exe")

```
#### Change TLD

YggTorrent TLD is change regularly, you can specify it at YggTorrentScraper construction with optionnal parameters yggtorrent_tld

``` python

from yggtorrentscraper import set_yggtorrent_tld

set_yggtorrent_tld("new_tld")

```

Session is requiered to download torrent

### Login (optionnal)

**I highly recommend you to not use your main account, YggTorrent ban bots**

Requiered only for download torrent's file

``` python

if(scraper.login("myidentifiant", "mypassword")):
    print("Login success")
else:
    print("Login failed")

```

### Search torrents

Return url's results torrent for specified search

``` python

torrents_url = scraper.search({"name" : "walking dead s08"})

"""

https://www2.yggtorrent.ch/torrent/filmvid▒o/s▒rie-tv/227730-the+walking+dead+s08+complete+vostfr+proper+720p+hdtv+x264-expm5
https://www2.yggtorrent.ch/torrent/filmvid▒o/s▒rie-tv/227752-the+walking+dead+s08+complete+vostfr+proper+hdtv+xvid-expm5
https://www2.yggtorrent.ch/torrent/filmvid▒o/s▒rie-tv/227763-the+walking+dead+s08+vostfr+web-dl+x264-ark01
https://www2.yggtorrent.ch/torrent/filmvid▒o/s▒rie-tv/227764-the+walking+dead+s08+vostfr+720p+amzn+web-dl+dd5+1+h264-ark01
https://www2.yggtorrent.ch/torrent/filmvid▒o/s▒rie-tv/227765-the+walking+dead+s08+vostfr+1080p+amzn+web-dl+ddp5+1+h264-ark01

...

"""

```

#### Search an torrents by uploader

Return url's results torrent for specified search

``` python

torrents_url = scraper.search({name : "walking dead s09", "uploader" : 'brandit'})

```

#### Search torrents with sorted results

Return url's results torrent for specified search

**YggTorrent's sorting is bugged, in general the results are sorted but sometimes you can find some torrents at a wrong position**

-   sort : name/publish_date/size/completed/seed/leech
-   order : asc/desc

``` python

torrents_url = scraper.search({"name": "blue oyster cult", "sort": "completed", "order": "desc"})

```

#### Search by category, subcategory and options_index

**Complete categories tree is available in file [categories.py](https://github.com/Harkame/YggTorrentScraper/blob/master/yggtorrentscraper/categories.py)**

``` python

parameters = {
    "name": "walking dead",
    "category": "films_&_videos",
    "subcategory": "serie_tv",
    "options": {
        "langue": {"francais_(vff/truefrench)"},
        "episode": {"saison_complete"},
        "qualite": {"bluray_[full]"},
    },
}


research = scraper.search(parameters)

```

### Most completed

Return url's of most completed (top 100) downloaded torrents

``` python

most_completed = scraper.most_completed()

"""

https://www2.yggtorrent.ch/torrent/filmvideo/serie-tv/440445-game-of-thrones-s08e02-multi-1080p-amzn-web-dl-dd5-1-x264-ark01
https://www2.yggtorrent.ch/torrent/application/windows/316475-microsoft-toolkit-v2-6-4-activateur-office-2016---2019-windows-10
https://www2.yggtorrent.ch/torrent/filmvideo/animation/431851-asterix-le-secret-de-la-potion-magique-2018-french-1080p-hdlight-x264-ac3-toxic
https://www2.yggtorrent.ch/torrent/application/windows/330032-windows-microsoft-office-2019-build-10730-20102-activation-francais
https://www2.yggtorrent.ch/torrent/filmvideo/serie-tv/436928-game-of-thrones-s08e01-multi-1080p-amzn-web-dl-dd5-1-h264-ark01

...

"""

```

### Details

Get torrent's details

``` python
torrent = scraper.extract_details('https://www2.yggtorrent.ch/torrent/filmvideo/serie-tv/440445-game-of-thrones-s08e02-multi-1080p-amzn-web-dl-dd5-1-x264-ark01')

print(torrent)

"""

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

"""

print(torrent.__str__(files=True, comments=True))

"""
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

"""

```

### Download

Download torrent's file (.torrent), requiered to be logged

``` python

if(scraper.login("myidentifiant", "mypassword")):
    print("Login success")

    torrent = scraper.extract_details('https://www2.yggtorrent.ch/torrent/filmvideo/serie-tv/440445-game-of-thrones-s08e02-multi-1080p-amzn-web-dl-dd5-1-x264-ark01')

    scraper.download_from_torrent(torrent)

    """
    OR
    """

    scraper.download_from_torrent_url('https://www2.yggtorrent.ch/torrent/filmvideo/serie-tv/440445-game-of-thrones-s08e02-multi-1080p-amzn-web-dl-dd5-1-x264-ark01')
else:
    print("Login failed")

```

### Logout (optionnal)

``` python

scraper.logout()

```

## TODO

-   More tests, find non bugged search (especially for sort tests)

## Test

Declare environment variables (requiered for login, download tests)

-   YGGTORRENT_IDENTIFIANT
-   YGGTORRENT_PASSWORD

``` bash

pip install tox

tox

```
