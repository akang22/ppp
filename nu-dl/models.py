"""Basic classes for use in application. Base API for scraping."""
from scrape import NovelUpdatesBase, SoupGeneral


class TranslatedLink:
    """Class representing an outbound link and metadata."""

    def __init__(
        self,
        link,
        name,
        author,
        date,
    ):
        self.link = link
        self.name = name
        self.author = author
        self.date = date


class NUInfo:
    """Class which gets information about a single light novel on NU."""

    def __init__(self, link):
        self.soup = SoupGeneral.get_soup(link)

        tot_pages = NovelUpdatesBase.get_pages_count(self.soup)
        self.links = NovelUpdatesBase.get_urls(self.soup)
        self.total_chapters = 0
        self.translated_up_to = 0
        self.original_lang = "japanese"
        self.original_src = ""
