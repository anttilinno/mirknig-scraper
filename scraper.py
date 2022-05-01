import re
import requests
import textwrap
from bs4 import BeautifulSoup

URL = "https://mirknig.su/knigi/programming"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

fetched_books = soup.find_all("td", class_="newsbody")


class Book:
    def __init__(self):
        pass


class Mir_Knig_Book(Book):
    book_fields_map = {
        "book_title": "Название",
        "book_author": "Автор",
        "book_publisher": "Издательство",
        "book_year": "Год",
        "book_format": "Формат",
        "book_pages": "Страниц",
        "book_file_size": "Размер",
        "book_language": "Язык",
    }

    def __init__(self):
        self.book_description = None
        self.book_image_link = None

        for k in self.book_fields_map.keys():
            setattr(self, k, None)

    def __str__(self):
        return (
            "-" * 80
            + f"\n|{'Title'.center(20)}|{self.book_title}\n"
            + "-" * 80
            + f"\n|{'Author'.center(20)}|{self.book_author}\n"
            + "-" * 80
            + f"\n|{'Publisher'.center(20)}|{self.book_publisher}\n"
            + "-" * 80
            + f"\n|{'Year'.center(20)}|{self.book_year}\n"
            + "-" * 80
            + f"\n|{'Format'.center(20)}|{self.book_format}\n"
            + "-" * 80
            + f"\n|{'Pages'.center(20)}|{self.book_pages}\n"
            + "-" * 80
            + f"\n|{'Size'.center(20)}|{self.book_file_size}\n"
            + "-" * 80
            + f"\n|{'Language'.center(20)}|{self.book_language}\n"
            + "-" * 80
            + "\n| "
            + "\n| ".join(textwrap.wrap(self.book_description))
            + "\n"
            + "-" * 80
        )

    def _parse_field(self, field, field_rus, raw_data):
        matches = re.search(
            "<b>" + field_rus + r":{0,1}</b>:{0,1}\s(.+?)(<br/>|$)", raw_data
        )
        if matches:
            setattr(self, field, matches[1])

    def _add_fields_info(self, rest_of_metadata):
        for k, v in self.book_fields_map.items():
            self._parse_field(k, v, rest_of_metadata)

    def _find_image(self, soup_book_record):
        self.image_link = soup_book_record.find("img")["src"]

    def _find_description(self, soup_book_record):
        book_raw_info = re.findall(
            ".*?(<!--TEnd-->|<!--dle_image_end-->)(.+)?<br\/><br\/>(.+)?</td>",
            str(soup_book_record),
        )
        self.book_description = book_raw_info[0][2].replace(r"<br/>", "\n")

        return book_raw_info[0][1]

    def add_metadata(self, soup_book_record):
        rest_of_metadata = self._find_description(soup_book_record)
        self._find_image(soup_book_record)
        self._add_fields_info(rest_of_metadata)


for book_rec in fetched_books:
    book = Mir_Knig_Book()
    book.add_metadata(book_rec)

    print(book, end="\n")
