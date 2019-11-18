import datetime
import logging
import os
import re

import requests
from bs4 import BeautifulSoup
from requests_toolbelt.multipart.encoder import MultipartEncoder

from .torrent import Torrent, TorrentComment, TorrentFile

__all__ = ["YggTorrentScraper", "YGGTORRENT_TLD", "YGGTORRENT_BASE_URL"]

YGGTORRENT_TLD = "pe"

YGGTORRENT_BASE_URL = f"https://www2.yggtorrent.{YGGTORRENT_TLD}"

YGGTORRENT_URL_LOGIN = f"{YGGTORRENT_BASE_URL}/user/login"
YGGTORRENT_URL_LOGOUT = f"{YGGTORRENT_BASE_URL}/user/logout"

logger = logging.getLogger("yggtorrentscraper")

YGGTORRENT_DOMAIN = ".yggtorrent.gg"
YGGTORRENT_TOKEN_COOKIE = "ygg_"

YGGTORRENT_SEARCH_URL = f"{YGGTORRENT_BASE_URL}/engine/search?name="

YGGTORRENT_SEARCH_URL = f"{YGGTORRENT_BASE_URL}/engine/search?name="

YGGTORRENT_SEARCH_URL_DESCRIPTION = "&description="
YGGTORRENT_SEARCH_URL_FILE = "&file="
YGGTORRENT_SEARCH_URL_UPLOADER = "&uploader="
YGGTORRENT_SEARCH_URL_CATEGORY = "&category="
YGGTORRENT_SEARCH_URL_SUB_CATEGORY = "&sub_category="
YGGTORRENT_SEARCH_URL_ORDER = "&order="
YGGTORRENT_SEARCH_URL_SORT = "&sort="
YGGTORRENT_SEARCH_URL_DO = "&do="
YGGTORRENT_SEARCH_URL_PAGE = "&page="

YGGTORRENT_SEARCH_URL_DESCRIPTION = "&description="
YGGTORRENT_SEARCH_URL_FILE = "&file="
YGGTORRENT_SEARCH_URL_UPLOADER = "&uploader="
YGGTORRENT_SEARCH_URL_CATEGORY = "&category="
YGGTORRENT_SEARCH_URL_SUB_CATEGORY = "&sub_category="
YGGTORRENT_SEARCH_URL_ORDER = "&order="
YGGTORRENT_SEARCH_URL_SORT = "&sort="
YGGTORRENT_SEARCH_URL_DO = "&do="
YGGTORRENT_SEARCH_URL_PAGE = "&page="

YGGTORRENT_GET_FILES = f"{YGGTORRENT_BASE_URL}/engine/get_files?torrent="
YGGTORRENT_GET_INFO = f"https://www2.yggtorrentchg/engine/get_nfo?torrent="

YGGTORRENT_MOST_COMPLETED_URL = f"{YGGTORRENT_BASE_URL}/engine/mostcompleted"

TORRENT_PER_PAGE = 50

YGGTORRENT_FILES_URL = f"{YGGTORRENT_BASE_URL}/engine/get_files?torrent="


class YggTorrentScraper:
    session = None

    def __init__(self, session, yggtorrent_tld=None):
        self.session = session

        if yggtorrent_tld is not None:
            YGGTORRENT_TLD = yggtorrent_tld

    def login(self, identifiant, password):
        """
        Login request with the specified identifiant and password, return an yggtorrent_token, necessary to download
        """
        self.session.cookies.clear()

        multipart_data = MultipartEncoder({"id": identifiant, "pass": password})

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection": "keep-alive",
            "Content-Type": "multipart/form-data; boundary=---------------------------255191561306",
            "Host": "www5.yggtorrent.pe",
            "TE": "Trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
            "X-Requested-With": "XMLHttpRequest",
        }

        response = self.session.post(
            YGGTORRENT_URL_LOGIN, data=multipart_data, headers=headers
        )

        logger.debug("status_code : %s", response.status_code)

        yggtorrent_token = None

        print(response.status_code)

        if response.status_code == 200:
            logger.debug("Login successful")
            yggtorrent_token = response.cookies.get_dict()[YGGTORRENT_TOKEN_COOKIE]

            cookie = requests.cookies.create_cookie(
                domain=YGGTORRENT_DOMAIN,
                name=YGGTORRENT_TOKEN_COOKIE,
                value=yggtorrent_token,
            )

            print(yggtorrent_token)

            self.session.cookies.set_cookie(cookie)

            return True
        else:
            logger.debug("Login failed")

            return False

    def logout(self):
        """
        Logout request
        """
        response = self.session.get(YGGTORRENT_URL_LOGOUT)

        self.session.cookies.clear()

        logger.debug("status_code : %s", response.status_code)

        if response.status_code == 200:
            logger.debug("Logout successful")

            return True
        else:
            logger.debug("Logout failed")

            return False

    def search(
        self,
        name=None,
        category="all",
        sub_category=None,
        descriptions=None,
        files=None,
        uploader=None,
        sort="publish_date",
        order="asc",
    ):

        search_url = create_search_url(
            name=name,
            category=category,
            sub_category=sub_category,
            descriptions=descriptions,
            files=files,
            uploader=uploader,
            sort=sort,
            order=order,
        )

        torrents_url = self.get_torrents_url(
            search_url=search_url,
            name=name,
            category=category,
            sub_category=sub_category,
            descriptions=descriptions,
            files=files,
            uploader=uploader,
            sort=sort,
            order=order,
        )

        return torrents_url

    def extract_details(self, torrent_url):
        """
        Extract informations from torrent's url
        """
        logger.debug("torrent_url : %s", torrent_url)

        torrents = []

        response = self.session.get(torrent_url)

        torrent_page = BeautifulSoup(response.content, features="lxml")

        torrent = Torrent()

        term_tags = torrent_page.find_all("a", {"class": "term"})

        for term_tag in term_tags:
            torrent.keywords.append(term_tag.text)

        connection_tags = torrent_page.find("tr", {"id": "adv_search_cat"}).find_all(
            "strong"
        )

        informations_tag = (
            torrent_page.find("table", {"class": "informations"})
            .find("tbody")
            .find_all("tr")
        )

        download_button = torrent_page.find("a", {"class": "butt"})

        if download_button.has_attr("href"):
            torrent.url = download_button["href"]

        torrent.seeders = int(connection_tags[0].text.replace(" ", ""))
        torrent.leechers = int(connection_tags[1].text.replace(" ", ""))
        torrent.completed = int(connection_tags[2].text.replace(" ", ""))

        torrent.name = informations_tag[0].find_all("td")[1].text
        torrent.size = informations_tag[3].find_all("td")[1].text
        torrent.uploader = informations_tag[5].find_all("td")[1].text

        mydatetime = re.search(
            "([0-9]*\/[0-9]*\/[0-9]* [0-9]*:[0-9]*)",
            informations_tag[6].find_all("td")[1].text,
            0,
        ).group(0)

        torrent.uploaded_datetime = datetime.datetime.strptime(
            mydatetime, "%d/%m/%Y %H:%M"
        )

        message_tags = torrent_page.find_all("div", {"class": "message"})

        for message_tag in message_tags:
            torrent_comment = TorrentComment()

            torrent_comment.author = message_tag.find("a").text
            torrent_comment.posted = message_tag.find("strong").text
            torrent_comment.text = message_tag.find(
                "span", {"id": "comment_text"}
            ).text.strip()

            torrent.comments.append(torrent_comment)

        torrents.append(torrent)

        torrent_id = torrent_page.find("form", {"id": "report-torrent"}).find(
            "input", {"type": "hidden", "name": "target"}
        )["value"]

        response = self.session.get(YGGTORRENT_GET_FILES + torrent_id)

        files_page = BeautifulSoup(response.content, features="lxml")

        file_tags = files_page.find_all("tr")

        for file_tag in file_tags:
            torrent_file = TorrentFile()

            td_tags = file_tag.find_all("td")

            torrent_file.file_size = (
                td_tags[0]
                .text.replace("\\r", "")
                .replace("\\n", "")
                .replace("\\t", "")
                .strip()
            )
            torrent_file.file_name = (
                td_tags[1]
                .text.replace("\\r", "")
                .replace("\\n", "")
                .replace("\\t", "")
                .replace("\\", "")
                .replace(" ", "")
                .strip()
            )

            torrent.files.append(torrent_file)

        return torrent

    def most_completed(self):
        """
        Return the most completed torrents url (TOP 100)
        """

        header = {"Accept": "application/json, text/javascript, */*; q=0.01"}
        self.session.post(YGGTORRENT_MOST_COMPLETED_URL, headers=header)

        json_response = self.session.post(
            YGGTORRENT_MOST_COMPLETED_URL, headers=header
        ).json()

        torrents_url = []

        for json_item in json_response:
            root = BeautifulSoup(json_item[1], features="lxml")

            a_tag = root.find("a")

            torrents_url.append(a_tag["href"])

        return torrents_url

    def get_torrents_url(
        self,
        search_url="",
        name=None,
        category="all",
        sub_category=None,
        descriptions=None,
        files=None,
        uploader=None,
        sort="date",
        order="asc",
        page=0,
        do="search",
    ):
        """
        Return
        """

        response = self.session.get(search_url)

        search_page = BeautifulSoup(response.content, features="lxml")

        pagination = search_page.find("ul", {"class": "pagination"})

        if pagination is None:
            limit_page = 1
        else:
            pagination_item = pagination.find_all("a")

            limit_page = int(pagination_item[-1]["data-ci-pagination-page"])

        torrents = []

        for page in range(0, limit_page):
            search_url = create_search_url(
                name=name,
                category=category,
                sub_category=sub_category,
                descriptions=descriptions,
                files=files,
                uploader=uploader,
                sort=sort,
                order=order,
                page=page * TORRENT_PER_PAGE,
            )

            response = self.session.get(search_url)

            search_page = BeautifulSoup(response.content, features="lxml")

            torrents_tag = search_page.findAll("a", {"id": "torrent_name"})

            for torrent_tag in torrents_tag:
                torrents.append(torrent_tag["href"])

        return torrents

    def download_from_torrent(self, torrent=None, destination_path="./"):
        if torrent is not None:
            return self.download_from_torrent_url(
                torrent_url=torrent.url, destination_path=destination_path
            )

    def download_from_torrent_url(self, torrent_url=None, destination_path="./"):
        response = self.session.get(YGGTORRENT_BASE_URL + torrent_url)

        temp_file_name = response.headers.get("content-disposition")

        file_name = temp_file_name[temp_file_name.index("filename=") + 10 : -1]

        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        file_full_path = os.path.join(destination_path, file_name)

        file = open(file_full_path, "wb")

        file.write(response.content)

        file.close()

        return file_full_path


def create_search_url(
    name=None,
    category="all",
    sub_category=None,
    descriptions=None,
    files=None,
    uploader=None,
    sort="publish_date",
    order="asc",
    page=0,
    do="search",
):
    """
    Return a formated URL for torrent's search
    """

    formated_search_url = YGGTORRENT_SEARCH_URL

    if name is not None:
        formated_search_url += name

    formated_search_url += YGGTORRENT_SEARCH_URL_CATEGORY
    formated_search_url += category

    formated_search_url += YGGTORRENT_SEARCH_URL_SUB_CATEGORY
    if sub_category is not None:
        formated_search_url += sub_category

    if page > 0:
        formated_search_url += YGGTORRENT_SEARCH_URL_PAGE
        formated_search_url += str(page)

    if descriptions is not None:
        formated_search_url += YGGTORRENT_SEARCH_URL_DESCRIPTION

        for description in descriptions:
            formated_search_url += description
            formated_search_url += "+"

    if files is not None:
        formated_search_url += YGGTORRENT_SEARCH_URL_FILE

        for file in files:
            formated_search_url += file
            formated_search_url += "+"

    if uploader is not None:
        formated_search_url += YGGTORRENT_SEARCH_URL_UPLOADER

        formated_search_url += uploader

    formated_search_url += YGGTORRENT_SEARCH_URL_SORT
    formated_search_url += sort

    formated_search_url += YGGTORRENT_SEARCH_URL_ORDER
    formated_search_url += order

    formated_search_url += YGGTORRENT_SEARCH_URL_DO
    formated_search_url += do

    return formated_search_url
