from fastapi.responses import HTMLResponse
import httpx
import re

from bs4 import BeautifulSoup
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


async def mirknig_raw_content(page: int = 1):
    URL = f"https://mirknig.su/knigi/programming/page/{page}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(URL)
        content = resp.content

    return content


async def mirknig_parse_book(book_rec):
    book_fields_map = {
        "title": "Название",
        "author": "Автор",
        "publisher": "Издательство",
        "year": "Год",
        "format": "Формат",
        "pages": "Страниц",
        "file_size": "Размер",
        "language": "Язык",
    }

    image_link = book_rec.find("img")["src"]
    book_raw_info = re.findall(
        r".*?(<!--TEnd-->|<!--dle_image_end-->)(.+)?<br/><br/>(.+)?</td>",
        str(book_rec),
    )
    book_description = book_raw_info[0][2]

    book_info = {"image": image_link, "description": book_description}

    for k, v in book_fields_map.items():
        matches = re.search(
            "<b>" + v + r":{0,1}</b>:{0,1}\s(.+?)(<br/>|$)", str(book_rec)
        )
        if matches:
            book_info[k] = matches[1]

    return book_info


async def parse_mirknig_content():

    content: str = await mirknig_raw_content()

    soup = BeautifulSoup(content, "html.parser")

    fetched_books = soup.find_all("td", class_="newsbody")

    return [await mirknig_parse_book(book_rec) for book_rec in fetched_books]


@app.get("/mirknig")
async def mirknig():
    t = await parse_mirknig_content()

    return {"data": t}


@app.get("/mirknig-rendered", response_class=HTMLResponse)
async def mirknig_template(request: Request):
    t = await parse_mirknig_content()

    return templates.TemplateResponse(
        "mirknig_books.jinja", {"request": request, "books": t}
    )
