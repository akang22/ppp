from ebooklib import epub
from models import NUInfo


def pad_zero(num, max_len):
    return "0" * (max_len - len(str(num))) + str(num)


def create_chapter(link, max_len):
    chapter = epub.EpubHtml(
        title=link.name,
        file_name=f"chap_{pad_zero(link.index, max_len)}_{link.name}.xhtml",
        lang="en",
    )
    chapter.content = f"<p>{link.scrape_text()}</p>"
    return chapter


def make_epub(nuinfo: NUInfo, output="./output"):
    book = epub.EpubBook()
    book.set_title(nuinfo.name)
    book.set_identifier(
        nuinfo.id,
    )
    book.set_language("en")
    for author in nuinfo.authors:
        book.add_author(author)
    max_len = len(str(len(chapters)))
    chapters = [create_chapter(link, max_len) for link in nuinfo.links]
    book.toc = ()
    for chapter in chapters:
        book.add_item(chapter)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    style = "BODY {color: white;}"
    nav_css = epub.EpubItem(
        uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style
    )
    book.add_item(nav_css)
    book.spine = ["nav", *chapters]
    epub.write_epub("test.epub", book, {})
