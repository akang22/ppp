from scrape import NovelUpdatesBase, SoupGeneral


class TranslatedLinks:
    def __init__(
        self,
        link,
        index,
    ):
        self.link = link
        self.index = 0
        self.name = "c1v1"
        self.author = "me"


class NUInfo:
    def __init__(self, link):
        self.soup = SoupGeneral.get_soup(link)

        tot_pages = NovelUpdatesBase.get_pages_count(self.soup)
        self.links = NovelUpdatesBase.get_urls(self.soup)
        self.total_chapters = 0
        self.translated_up_to = 0
        self.original_lang = "japanese"
        self.original_src = ""
