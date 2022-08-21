"""Basic classes for use in application. Base API for scraping."""
import scrape


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
        self.soup = scrape.SoupGeneral.get_soup(link)

        tot_pages = scrape.NovelUpdatesBase.get_pages_count(self.soup)

        # TODO: multithread
        self.links = reversed([
            chap_link
            for page_number in range(1, tot_pages + 1)
            for chap_link in scrape.NovelUpdatesBase.get_urls(
                scrape.SoupGeneral.get_soup(link, page=page_number)
            )
        ])

        self.chapter_count = len(self.links)
        self.complete = scrape.NovelUpdatesBase.get_status(self.soup)
        self.original_lang = scrape.NovelUpdatesBase.get_language(self.soup)
        self.original_src = ""
