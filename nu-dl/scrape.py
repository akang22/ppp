import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

# move to utils later


def filtersoup(**soup_identifiers):
    return lambda func: lambda soup: func(soup.find(**soup_identifiers))


def catch(func, *args, ExceptionType=Exception, handle=lambda e: e, **kwargs):
    try:
        return func(*args, **kwargs)
    except ExceptionType as e:
        return handle(e)


# end utils


class SoupGeneral:
    @staticmethod
    def get_soup(link):
        req = Request(link, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req).read()
        return BeautifulSoup(page, features="html.parser")


class NovelUpdatesBase:
    @staticmethod
    @filtersoup(class_="digg_pagination")
    def get_url_pages(soup):
        return max(
            [
                catch(
                    lambda elem: int(elem.text),
                    a_node,
                    ExceptionType=ValueError,
                    handle=lambda e: 0,
                )
                for a_node in soup.findAll("a")
            ]
        )

    @staticmethod
    def get_urls(soup):
        links = [
            link.get("href")
            for link in soup.findAll(
                "a", attrs={"href": re.compile("^//www.novelupdates.com/extnu")}
            )
        ]
        return links

    @staticmethod
    def get_lang(soup):
        pass
