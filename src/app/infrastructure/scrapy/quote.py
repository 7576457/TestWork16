import httpx
from app.domain.quote.entity import Quote
from app.domain.quote.service import QuoteService
from bs4 import BeautifulSoup
import uuid


class ParseQuotesService(QuoteService):
    def __init__(self):
        self.base_url = "https://quotes.toscrape.com"

    async def parse(self) -> list[Quote]:
        quotes = []
        page = 1

        async with httpx.AsyncClient() as client:
            while True:
                url = f"{self.base_url}/page/{page}/" if page > 1 else self.base_url
                response = await client.get(url)

                if response.status_code != 200:
                    break

                page_quotes = self._proccess(response.text)
                if not page_quotes:
                    break

                quotes.extend(page_quotes)
                page += 1

        return quotes

    def _proccess(self, html: str) -> list[Quote]:
        soup = BeautifulSoup(html, "html.parser")
        quotes = []

        for quote_div in soup.find_all("div", class_="quote"):
            try:
                text_elem = quote_div.find("span", class_="text")
                if not text_elem:
                    continue
                text = text_elem.get_text().strip()
                if text.startswith('"') and text.endswith('"'):
                    text = text[1:-1]

                author_elem = quote_div.find("small", class_="author")
                if not author_elem:
                    continue
                author = author_elem.get_text().strip()
                tag_elems = quote_div.find_all("a", class_="tag")
                raw_tags = [tag.get_text().strip() for tag in tag_elems]
                tags = [tag.replace(" ", "-") for tag in raw_tags if tag.strip()]

                quote = Quote(uuid=uuid.uuid4(), author=author, text=text, tags=tags)
                quotes.append(quote)

            except Exception as e:
                print(f"Parse error: {e}")
                continue

        return quotes
