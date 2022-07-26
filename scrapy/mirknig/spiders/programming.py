import re
import scrapy

from ..items import MirknigItem


class ProgrammingSpider(scrapy.Spider):
    name = "programming"
    allowed_domains = ["mirknig.su"]
    start_urls = ["https://mirknig.su/knigi/programming"]

    page_book_fields = {
        "title": rf"^.*?<b>Название:{{0,1}}</b>:{{0,1}}\s(.*?)<br>",
        "author": rf"^.*?<b>Автор:{{0,1}}</b>:{{0,1}}\s(.*?)<br>",
        "publisher": rf"^.*?<b>Издательство:{{0,1}}</b>:{{0,1}}\s(.*?)<br>",
        "year": rf"^.*?<b>Год:{{0,1}}</b>:{{0,1}}\s(.*?)<br>",
        "digital_format": rf"^.*?<b>Формат:{{0,1}}</b>:{{0,1}}\s(.*?)<br>",
        "pages": rf"^.*?<b>Страниц:{{0,1}}</b>:{{0,1}}\s(.*?)<br>",
        "size": rf"^.*?<b>Размер:{{0,1}}</b>:{{0,1}}\s(.*?)<br>",
        "language": rf"^.*?<b>Язык:{{0,1}}</b>:{{0,1}}\s(.*?)<br>",
        "description": rf"<br><br>(.*?)</td>",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = MirknigItem()

        for book in response.css("td.newsbody"):
            items["image"] = {"image": book.css("img::attr(src)").get()}

            raw_book_info = book.get()

            for k, v in self.page_book_fields.items():
                result = re.search(
                    self.page_book_fields[k],
                    raw_book_info,
                )

                if result is None:
                    continue

                items[k] = result.group(1).strip()

            yield items
