from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re

def getUrls(list_url):
    req = Request(list_url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, features="html.parser")
    links = [link.get('href') for link in soup.findAll('a', attrs={'href': re.compile("^//www.novelupdates.com/extnu")})]
    return links
