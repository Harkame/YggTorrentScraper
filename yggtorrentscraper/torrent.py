import os


class Torrent:
    """
    Torrent entity
    """

    name = None
    uploaded_datetime = None
    size = None
    uploader = None

    keywords = []

    completed = -1
    seeders = -1
    leechers = -1

    url = None
    download_url = None

    files = []
    comments = []

    def __str__(self, comments=False, files=False):
        to_string = ""

        to_string += "Name      : "
        to_string += self.name
        to_string += os.linesep

        to_string += "Url       : "

        if self.url is not None:
            to_string += self.url
        else:
            to_string += "N/A"

        if self.download_url is not None:
            to_string += self.download_url
        else:
            to_string += "N/A"

        to_string += os.linesep
        to_string += os.linesep

        to_string += f"Keywords ({len(self.keywords)})  : "
        to_string += os.linesep

        for keyword in self.keywords:
            to_string += f"- {keyword}"
            to_string += os.linesep

        to_string += os.linesep

        to_string += "Uploaded  : "
        to_string += str(self.uploaded_datetime)
        to_string += os.linesep

        to_string += "Size      : "
        to_string += str(self.size)
        to_string += os.linesep

        to_string += "Uploader  : "
        to_string += self.uploader
        to_string += os.linesep

        to_string += "Completed : "
        to_string += str(self.completed)
        to_string += os.linesep

        to_string += "Seeders   : "
        to_string += str(self.seeders)
        to_string += os.linesep

        to_string += "Leechers  : "
        to_string += str(self.leechers)
        to_string += os.linesep

        to_string += os.linesep

        to_string += f"Files ({len(self.files)})"
        to_string += os.linesep

        if files:
            for file in self.files:
                to_string += str(file)
                to_string += os.linesep

        to_string += os.linesep

        to_string += f"Comments ({len(self.comments)})"
        to_string += os.linesep

        if comments:
            for comment in self.comments:
                to_string += str(comment)
                to_string += os.linesep

        return to_string


class TorrentFile:

    """
    Torrent's file entity
    """

    size = ""
    file_name = ""

    def __str__(self):
        to_string = ""

        to_string += "size      : "
        to_string += self.size
        to_string += os.linesep

        to_string += "file_name : "
        to_string += self.file_name
        to_string += os.linesep

        return to_string


class TorrentComment:

    """
    Torrent's comment entity
    """

    author = ""
    posted = ""
    text = ""

    def __str__(self):
        to_string = ""

        to_string += "Author : "
        to_string += self.author
        to_string += os.linesep

        to_string += "Posted : "
        to_string += str(self.posted)
        to_string += os.linesep

        to_string += "Text   : "
        to_string += str(self.text)
        to_string += os.linesep

        return to_string
