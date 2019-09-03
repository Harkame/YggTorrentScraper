YggTorrentDownloader
====================

|Codacy Badge| |Build Status| |License: GPL v3| |codecov|

Installation
------------

.. code:: bash

   pip install yggtorrentscraper

   OR

   python setup.py install

Dependencies
~~~~~~~~~~~~

-  `Beautiful Soup 4`_

-  `PyYAML`_

-  `lxml`_

-  `Requests`_

Usage
-----

.. code-block:: python

  import requests
  from yggtorrentscraper import YggTorrentScraper

  yggtorrentscraper = YggTorrentScraper(requests.session())

  yggtorrentscraper.login(identifiant='myidentifiant', password='mypassword')

  most_completed = yggtorrentscraper.most_completed()

  torrent = yggtorrentscraper.extract_details(most_completed[0])

  print(torrent.__str__(files=False, comments=False))

  yggtorrentscraper.download_from_torrent(torrent=torrent, destination_path='./')

  yggtorrentscraper.logout()

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
