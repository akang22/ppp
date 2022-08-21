import json
import os
import re
import subprocess
import tempfile
import time
import unicodedata
from urllib.request import Request, urlopen


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def parse_article(link, refresh_time=60):
    """Interface with readabilityjs to extract article."""
    # Loosely based off 'https://github.com/alan-turing-institute/ReadabiliPy/blob/master/readabilipy/simple_json.py'.
    req = Request(link, headers={"User-Agent": "Mozilla/5.0"})
    html = str(urlopen(req).read())
    temp_path = os.path.join(tempfile.gettempdir(), "nudltoreadabilityjsinterface")
    file_name = slugify(link)
    finished_file = os.path.join(temp_path, file_name + ".json")
    return_json = {
        "title": None,
        "byline": None,
        "date": None,
        "content": None,
        "plain_content": None,
        "plain_text": None,
    }

    if (
        os.path.exists(finished_file)
        and os.path.getmtime(finished_file) + refresh_time * 1000 > time.time()
    ):
        with open(finished_file, "r") as file:
            return_json.update(json.loads(file.read()))
        return return_json
    
    os.makedirs(temp_path, exist_ok=True)

    write_path = os.path.join(temp_path, file_name)

    with open(write_path, "w") as file:
        file.write(html)

    subprocess.check_call(["node", "parse_article.js", write_path])

    os.remove(write_path)

    # yes I know this is dupliicated from above.
    # This is just a temporary solution until i port readability over to python in its own ppp.
    # yes, there's nothing more permanent than a temporary solution. Check git blame.
    with open(finished_file, "r") as file:
        return_json.update(json.loads(file.read()))

    return return_json
