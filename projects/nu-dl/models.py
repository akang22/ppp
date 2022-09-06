"""Basic classes for use in application. Base API for scraping."""
import itertools
import scrape
import parse_translation
from urllib.request import Request, urlopen


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
        self.text = None
        self.index = None
        req = Request(link, headers={"User-Agent": "Mozilla/5.0"})
        self.html = str(
            urlopen(req).read(),
        )

    def scrape_text(self):
        """Scrapes text body from website. No network request is made"""
        self.text = parse_translation.parse_article(self.link, html=self.html)

    def add_index(self, index):
        self.index = index
        return self


class NUInfo:
    """Class which gets information about a single light novel on NU."""

    def __init__(self, link):
        self.soup = scrape.SoupGeneral.get_soup(link)

        self.complete = scrape.NovelUpdatesBase.get_status(self.soup)
        self.original_lang = scrape.NovelUpdatesBase.get_language(self.soup)
        self.original_src = ""
        self.title = scrape.NovelUpdatesBase.get_title(self.soup)
        self.id = scrape.NovelUpdatesBase.parse_id(link)

        tot_pages = scrape.NovelUpdatesBase.get_pages_count(self.soup)

        index_gen = itertools.count(start=1)

        # TODO: multithread
        self.links = [
            chap_link.add_index(next(index_gen))
            for page_number in reversed(range(1, tot_pages + 1))
            for chap_link in reversed(
                scrape.NovelUpdatesBase.get_urls(
                    scrape.SoupGeneral.get_soup(link, page=page_number)
                )
            )
        ]

        self.chapter_count = len(self.links)
        self.authors = self.get_authors()

    def get_authors(self):
        """Get list of all author groups."""
        authors = {}
        for link in self.links:
            authors.add(link.author)
        return sorted(list(authors))

    def get_texts_for_all_chapters(self):
        """Take each chapter and get its text."""
        # TODO: multihtread
        for link in self.links:
            link.scrape_text()
