import datetime
import logging
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

from torrent import Torrent, TorrentComment, TorrentFile
from categories import categories

YGGTORRENT_TLD = "ws"

YGGTORRENT_BASE_URL = f"https://www2.yggtorrent.{YGGTORRENT_TLD}"

YGGTORRENT_LOGIN_URL = f"{YGGTORRENT_BASE_URL}/user/login"
YGGTORRENT_LOGOUT_URL = f"{YGGTORRENT_BASE_URL}/user/logout?attempt=1"

YGGTORRENT_SEARCH_URL = f"{YGGTORRENT_BASE_URL}/engine/search?name="

logger = logging.getLogger("yggtorrentscraper")

YGGTORRENT_DOMAIN = f".yggtorrent.{YGGTORRENT_TLD}"
YGGTORRENT_TOKEN_COOKIE = "ygg_"

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


def change_yggtorrent_tld(yggtorrent_tld=None):
    """
    Redefine all string variable according to new TLD
    """

    global YGGTORRENT_TLD
    global YGGTORRENT_BASE_URL
    global YGGTORRENT_LOGIN_URL
    global YGGTORRENT_SEARCH_URL
    global YGGTORRENT_DOMAIN
    global YGGTORRENT_GET_FILES
    global YGGTORRENT_GET_INFO
    global YGGTORRENT_MOST_COMPLETED_URL
    global YGGTORRENT_FILES_URL

    YGGTORRENT_TLD = yggtorrent_tld

    YGGTORRENT_BASE_URL = f"https://www2.yggtorrent.{YGGTORRENT_TLD}"

    YGGTORRENT_LOGIN_URL = f"{YGGTORRENT_BASE_URL}/user/login"
    YGGTORRENT_SEARCH_URL = f"{YGGTORRENT_BASE_URL}/user/logout"

    YGGTORRENT_SEARCH_URL = f"{YGGTORRENT_BASE_URL}/engine/search?name="

    YGGTORRENT_DOMAIN = ".yggtorrent.gg"

    YGGTORRENT_GET_FILES = f"{YGGTORRENT_BASE_URL}/engine/get_files?torrent="
    YGGTORRENT_GET_INFO = f"https://www2.yggtorrentchg/engine/get_nfo?torrent="

    YGGTORRENT_MOST_COMPLETED_URL = f"{YGGTORRENT_BASE_URL}/engine/mostcompleted"

    YGGTORRENT_FILES_URL = f"{YGGTORRENT_BASE_URL}/engine/get_files?torrent="


class YggTorrentScraper:
    session = None

    def __init__(self, session):
        self.session = session

    def login(self, identifiant, password):
        """
        Login request with the specified identifiant and password, return an yggtorrent_token, necessary to download
        """
        self.session.cookies.clear()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "PostmanRuntime/7.17.1",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
            "Host": f"www5.yggtorrent.{YGGTORRENT_TLD}",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

        response = self.session.post(
            YGGTORRENT_LOGIN_URL,
            data={"id": identifiant, "pass": password},
            headers=headers,
        )

        logger.debug("status_code : %s", response.status_code)

        yggtorrent_token = None

        if response.status_code == 200:
            logger.debug("Login successful")
            yggtorrent_token = response.cookies.get_dict()[YGGTORRENT_TOKEN_COOKIE]

            cookie = requests.cookies.create_cookie(
                domain=YGGTORRENT_DOMAIN,
                name=YGGTORRENT_TOKEN_COOKIE,
                value=yggtorrent_token,
            )

            self.session.cookies.set_cookie(cookie)

            return True
        else:
            logger.debug("Login failed")

            return False

    def logout(self):
        """
        Logout request
        """
        response = self.session.get(YGGTORRENT_LOGOUT_URL)

        self.session.cookies.clear()

        logger.debug("status_code : %s", response.status_code)

        if response.status_code == 200:
            logger.debug("Logout successful")

            return True
        else:
            logger.debug("Logout failed")

            return False

    def search(self, parameters):
        search_url = create_search_url(parameters)

        torrents_url = self.get_torrents_url(search_url, parameters)

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

    def get_torrents_url(self, search_url, parameters):
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
            parameters["page"] = page * TORRENT_PER_PAGE

            search_url = create_search_url(parameters)

            response = self.session.get(search_url)

            search_page = BeautifulSoup(response.content, features="lxml")

            torrents_tag = search_page.findAll("a", {"id": "torrent_name"})

            for torrent_tag in torrents_tag:
                torrents.append(torrent_tag["href"])

        return torrents

    def download_from_torrent_url(self, torrent_url=None, destination_path="./"):
        if torrent_url is not None:
            torrent = self.extract_details(torrent_url)

            return self.download_from_torrent_download_url(
                torrent_url=torrent.url, destination_path=destination_path
            )

    def download_from_torrent(self, torrent=None, destination_path="./"):
        if torrent is not None:
            return self.download_from_torrent_download_url(
                torrent_url=torrent.url, destination_path=destination_path
            )

    def download_from_torrent_download_url(
        self, torrent_url=None, destination_path="./"
    ):
        if torrent_url is None:
            raise Exception("Invalid torrent_url, make sure you are logged")

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


def create_search_url(parameters):
    """
    Return a formated URL for torrent's search
    """

    formated_search_url = YGGTORRENT_SEARCH_URL

    if "name" in parameters:
        formated_search_url += parameters["name"]

    if "category" in parameters:
        formated_search_url += YGGTORRENT_SEARCH_URL_CATEGORY
        formated_search_url += parameters["category"]

    if "sub_category" in parameters:
        formated_search_url += YGGTORRENT_SEARCH_URL_SUB_CATEGORY
        formated_search_url += parameters["sub_category"]

    if "page" in parameters:
        formated_search_url += YGGTORRENT_SEARCH_URL_PAGE
        formated_search_url += str(parameters["page"])

    if "descriptions" in parameters:
        formated_search_url += YGGTORRENT_SEARCH_URL_DESCRIPTION

        for description in parameters["descriptions"]:
            formated_search_url += description
            formated_search_url += "+"

    if "files" in parameters:
        formated_search_url += YGGTORRENT_SEARCH_URL_FILE

        for file in parameters["files"]:
            formated_search_url += file
            formated_search_url += "+"

    if "uploader" in parameters:
        formated_search_url += YGGTORRENT_SEARCH_URL_UPLOADER
        formated_search_url += parameters["uploader"]

    if "sort" in parameters:
        formated_search_url += YGGTORRENT_SEARCH_URL_SORT
        formated_search_url += parameters["sort"]

    if "order" in parameters:
        formated_search_url += YGGTORRENT_SEARCH_URL_ORDER
        formated_search_url += parameters["order"]

        id_category = "all"
        id_subcategory = "all"
        fields_index = []

    id_category = ""
    id_subcategory = ""
    fields_index = []

    if "category" in parameters:
        for category in categories:
            if parameters["category"] == category["name"]:
                formated_search_url += YGGTORRENT_SEARCH_URL_CATEGORY
                formated_search_url += category["id"]

                if "subcategory" in parameters:
                    for subcategory in category["subcategories"]:
                        if parameters["subcategory"] == subcategory["name"]:
                            formated_search_url += YGGTORRENT_SEARCH_URL_SUB_CATEGORY
                            formated_search_url += subcategory["id"]
                            if "fields" in parameters:
                                for key, values in parameters["fields"].items():
                                    for field in subcategory["fields"]:
                                        if key == field["name"]:
                                            for searched_value in values:
                                                for index, value in enumerate(
                                                    field["values"]
                                                ):
                                                    if searched_value == value:
                                                        fields_index.append(index)

    formated_search_url += YGGTORRENT_SEARCH_URL_DO
    formated_search_url += "search"

    return formated_search_url


"""
https://www2.yggtorrent.ws/engine/search?name=walking+dead&description=&file=&uploader=&category=2145&sub_category=2184&do=search
https://www2.yggtorrent.ws/engine/search?name=walking+dead&description=&file=&uploader=&category=2145&sub_category=2178&option_langue%3Amultiple[]=1&do=search
https://www2.yggtorrent.ws/engine/search?name=walking+dead&description=&file=&uploader=&category=2145&sub_category=2178&option_langue%3Amultiple[]=2&do=search
https://www2.yggtorrent.ws/engine/search?name=walking+dead&description=&file=&uploader=&category=2145&sub_category=2178&option_langue%3Amultiple[]=1&option_langue%3Amultiple[]=2&do=search

"""
if __name__ == "__main__":
    scraper = YggTorrentScraper(requests.session())

    search_url = create_search_url(
        {
            "name": "walking dead",
            "category": "films_&_videos",
            "subcategory": "animation",
            "fields": {"langue": {"anglais", "vostfr"}},
        }
    )

    print(search_url)
