import requests

def parse_article(link):
    html = requests.get(link).text

