import datetime
import logging
import os
import re

import requests
from bs4 import BeautifulSoup

from torrent import Torrent, TorrentComment, TorrentFile
from categories import categories

import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from random import randint

YGGTORRENT_TLD = "se"

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


def set_yggtorrent_tld(yggtorrent_tld=None):
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


def get_yggtorrent_tld():
    return YGGTORRENT_TLD


class YggTorrentScraperSelenium:
    def __init__(self, driver=None):
        self.session = None
        self.driver = driver

    def login(self, identifiant, password):
        self.driver.get(YGGTORRENT_BASE_URL)
        WebDriverWait(self.driver, 30000).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#title"))
        )

        register_button = self.driver.find_element_by_css_selector("#register")

        self.driver.execute_script("arguments[0].click();", register_button)

        input_identifiant = self.driver.find_element_by_css_selector("input[name='id']")

        input_identifiant.clear()
        input_identifiant.send_keys(identifiant)

        input_password = self.driver.find_element_by_css_selector("input[name='pass']")

        input_password.clear()
        input_password.send_keys(password)

        login_button = self.driver.find_element_by_css_selector("#user-login button")

        self.driver.execute_script("arguments[0].click();", login_button)

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

        self.driver.get(torrent_url)

        WebDriverWait(self.driver, 30000).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#title"))
        )

        torrents = []

        # response = self.session.get(torrent_url)

        torrent_page = BeautifulSoup(self.driver.page_source, features="lxml")

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

        # response = self.session.get(YGGTORRENT_GET_FILES + torrent_id)

        self.driver.get(torrent_url)

        WebDriverWait(self.driver, 30000).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#informationsContainer"))
        )

        files_page = BeautifulSoup(self.driver.page_source, features="lxml")

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

        self.driver.get(YGGTORRENT_MOST_COMPLETED_URL)

        WebDriverWait(self.driver, 30000).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#DataTables_Table_0_wrapper")
            )
        )

        torrents_url = []

        root = BeautifulSoup(self.driver.page_source, features="lxml")

        tbody_element = root.find("tbody")

        tr_elements = tbody_element.find_all("tr")

        for tr_element in tr_elements:
            a_elements = tr_element.find_all("a")

            a_element = a_elements[1]
            torrents_url.append(a_element["href"])

        driver.quit()

        return torrents_url

    def get_torrents_url(self, search_url, parameters):
        """
        Return
        """

        self.driver.get(search_url)

        WebDriverWait(self.driver, 30000).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#criteriarecherche"))
        )

        search_page = BeautifulSoup(self.driver.page_source, features="lxml")

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

            self.driver.get(search_url)

            WebDriverWait(self.driver, 30000).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#over-18-notification")
                )
            )

            search_page = BeautifulSoup(self.driver.page_source, features="lxml")

            torrents_tag = search_page.findAll("a", {"id": "torrent_name"})

            for torrent_tag in torrents_tag:
                torrents.append(torrent_tag["href"])

        return torrents

    def download_from_torrent_url(self, torrent_url=None, destination_path="./"):
        if torrent_url is not None:
            self.driver.get(torrent_url)

            WebDriverWait(self.driver, 30000).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#title"))
            )

            download_button = self.driver.find_element_by_css_selector("a.butt")

            self.driver.execute_script("arguments[0].click();", download_button)

    def download_from_torrent_download_url(
        self, torrent_url=None, destination_path="./"
    ):
        if torrent_url is None:
            raise Exception("Invalid torrent_url, make sure you are logged")

        cookies = driver.get_cookies()

        self.session = requests.Session()
        for cookie in cookies:
            self.session.cookies.set(cookie["name"], cookie["value"])

        headers = {
            "User-Agent": "PostmanRuntime/7.17.1",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
            "Host": f"www.yggtorrent.{YGGTORRENT_TLD}",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

        response = self.session.get(torrent_url, headers=headers)

        print(response.status_code)

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
        formated_search_url += parameters["name"].replace(" ", "+")

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
                            if "options" in parameters:
                                for key, values in parameters["options"].items():
                                    for option in subcategory["options"]:
                                        if key == option["name"]:
                                            for searched_value in values:
                                                for index, value in enumerate(
                                                    option["values"]
                                                ):
                                                    if searched_value == value:
                                                        formated_search_url += (
                                                            "&option_"
                                                        )
                                                        formated_search_url += option[
                                                            "name"
                                                        ]
                                                        # options_index.append(index)
                                                        if "multiple" in option:
                                                            formated_search_url += (
                                                                "%3Amultiple"
                                                            )

                                                        formated_search_url += "[]="
                                                        formated_search_url += str(
                                                            index + 1
                                                        )

    formated_search_url += YGGTORRENT_SEARCH_URL_DO
    formated_search_url += "search"

    return formated_search_url


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("headless")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome("D:\chromedriver.exe", options=options)

    scraper = YggTorrentScraperSelenium(driver=driver)
    scraper.login("harkame573", "Palavas34250")
    # print(scraper.most_completed())

    # print(scraper.search({"name": "walking dead"}))
    """
    scraper.download_from_torrent_url(
        "https://www2.yggtorrent.se/torrent/ebook/livres/301724-robert+kirkman+jay+bonansinga+-+the+walking+dead+-+tome+8+retour+à+woodbury+epub"
    )
    """
    scraper.download_from_torrent_download_url(
        "https://www2.yggtorrent.se/engine/download_torrent?id=301724", "./"
    )

    """
    torrent = scraper.extract_details(
        "https://www2.yggtorrent.se/torrent/ebook/livres/301724-robert+kirkman+jay+bonansinga+-+the+walking+dead+-+tome+8+retour+à+woodbury+epub"
    )

    print(torrent)
    """
