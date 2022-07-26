use std::collections::HashMap;

fn main() {
    let response = reqwest::blocking::get("https://mirknig.su/knigi/programming/")
        .unwrap()
        .text()
        .unwrap();

    let document = scraper::Html::parse_document(&response);

    let book_selector = scraper::Selector::parse("td.newsbody").unwrap();

    let _mirknig_book_fields = HashMap::from([
        ("title", r"^.*?<b>Название:{0,1}</b>:{0,1}\s(.*?)<br>"),
        ("author", r"^.*?<b>Автор:{0,1}</b>:{0,1}\s(.*?)<br>"),
        (
            "publisher",
            r"^.*?<b>Издательство:{0,1}</b>:{0,1}\s(.*?)<br>",
        ),
        ("year", r"^.*?<b>Год:{0,1}</b>:{0,1}\s(.*?)<br>"),
        ("format", r"^.*?<b>Формат:{0,1}</b>:{0,1}\s(.*?)<br>"),
        ("pages", r"^.*?<b>Страниц:{0,1}</b>:{0,1}\s(.*?)<br>"),
        ("file_size", r"^.*?<b>Размер:{0,1}</b>:{0,1}\s(.*?)<br>"),
        ("language", r"^.*?<b>Язык:{0,1}</b>:{0,1}\s(.*?)<br>"),
        ("description", r"<br><br>(.*?)</td>"),
    ]);

    let books = document.select(&book_selector).map(|x| x.inner_html());
    books.for_each(|item| println!("{}", item));

    for book in document.select(&book_selector) {
        println!("{:?}", book.text().collect::<Vec<_>>());
        // for (key, val) in &mirknig_book_fields {
        //     let re = Regex::new(&val).unwrap();
        // }
    }
}
