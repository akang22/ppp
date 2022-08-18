"""Provides static functions to parse HTML"""
import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import models

# Following functions/classes aren't really scraping, could be moved to utils folder


def filtersoup(**soup_identifiers):
    """Decorator to filter BeautifulSoup html."""
    return lambda func: lambda soup, **kwargs: func(
        soup.find(**soup_identifiers), *kwargs
    )


def catch(func, *args, ExceptionType=Exception, handle=lambda e: e, **kwargs):
    """Helper function to handle exceptions in list comprehension."""
    try:
        return func(*args, **kwargs)
    except ExceptionType as e:
        return handle(e)


class SoupGeneral:
    """Soup utility functions related to Soup which don't involve scraping."""

    @staticmethod
    def get_soup(link, page: int = None):
        """"""
        if page is not None:
            link += f"?pg={page}"
        req = Request(link, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(req).read()
        return BeautifulSoup(page, features="html.parser")


class NovelUpdatesBase:
    """Scraping functions for base novelupdates website"""

    @staticmethod
    @filtersoup(class_="digg_pagination")
    def get_pages_count(soup):
        """Get count of table pages on website."""
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
    @filtersoup(id="myTable")
    def get_urls(soup):
        """Return list of link objects to translated chapters."""
        for row in soup.findAll("tr"):
            # make info
            pass

        links = [
            link.get("href")
            for link in soup.findAll(
                "a", attrs={"href": re.compile("^//www.novelupdates.com/extnu")}
            )
        ]
        return links

    @staticmethod
    def get_lang(soup):
        """Return language of article"""
        pass
