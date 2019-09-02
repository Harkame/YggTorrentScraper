YggTorrentDownloader
====================

|Codacy Badge| |Build Status| |License: GPL v3| |codecov|

Installation
------------

.. code:: bash

   pip install -r requirements.txt

Dependencies
~~~~~~~~~~~~

-  `Beautiful Soup 4`_

-  `PyYAML`_

-  `lxml`_

-  `Requests`_

Usage
-----

Run
~~~

.. code:: bash

   python yggtorrentdownloader/main.py -i myidentifiant -p mypassword

Options
~~~~~~~

.. code:: bash

  usage: main.py [-h] [-c CONFIG_FILE] [-d DESTINATION_PATH] [-T TLD] [-v] -i IDENTIFIANT -p PASSWORD

  Script to download torrents from YggTorrent

  optional arguments:
    -h, --help            show this help message and exit
    -c CONFIG_FILE, --config_file CONFIG_FILE
                          Set config file
                          Example : python yggtorrentscraper/main.py -c /home/myconfigfile.yml
    -d DESTINATION_PATH, --destination_path DESTINATION_PATH
                          Set destination path of downloaded torrents
                          Example : python yggtorrentscraper/main.py -d /home/torrents/
    -T TLD, --tld TLD     Set yggtorrent TLD manualy (because yggtorrent change often)
                          Example : python yggtorrentscraper/main.py -T ch
    -v, --verbose         Active verbose mode, support different level
                          Example : python yggtorrentscraper/main.py -vv
    -i IDENTIFIANT, --identifiant IDENTIFIANT
                          YggTorrent account identifiant
                          Example : python yggtorrentscraper/main.py -i myidentifiant
    -p PASSWORD, --password PASSWORD
                          YggTorrent account password
                          Example : python yggtorrentscraper/main.py -p mypassword

How it work
~~~~~~~~~~~

This program use an config file (default : ./config.yml)

This file contains list of torrent to download, destination path, etc.

Example of config file
^^^^^^^^^^^^^^^^^^^^^^

.. code:: yaml

   list_research:
     - research:
       name:
         The.Walking.Dead.S09
       limit:
         5

     - research:
       name:
         test
       files:
         - avi
         - mkv
       uploaders:
         - uploader1
         - uploader2
       descriptions:
           - description1
           - description2
       sort: #name|publish_date|size|completed|seed|leech
         size
       order: #asc|desc
         desc
       limit:
         1

   destination_path:
     ./torrents

Download torrents
~~~~~~~~~~~~~~~~~

TODO
~~~~~~~

- Fix encoding

- Special research (top 100, etc)

Add an entry research to attribute list_research

All sub-attributes are optionnal, but i reccomend to keep
sub-attribute limit

.. _Beautiful Soup 4: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
.. _PyYAML: https://github.com/yml/pyyml
.. _lxml: https://github.com/lxml/lxml.git
.. _Requests: https://github.com/kennethreitz/requests

.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/791c3f45639c4031a261b76df866d0db
   :target: https://www.codacy.com/app/Harkame/YggTorrentDownloader?utm_source=github.com&utm_medium=referral&utm_content=Harkame/YggTorrentDownloader&utm_campaign=Badge_Grade
.. |Build Status| image:: https://travis-ci.org/Harkame/YggTorrentDownloader.svg?branch=master
   :target: https://travis-ci.org/Harkame/YggTorrentDownloader
.. |License: GPL v3| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0
.. |codecov| image:: https://codecov.io/gh/Harkame/YggTorrentDownloader/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Harkame/YggTorrentDownloader
