import logging

import requests
from bs4 import BeautifulSoup

from scripts.utils import BaseTask


class Task(BaseTask):
    """
    A class that represents a task to scrape data from the Mercado Livre website and store it in a MongoDB collection.
    """

    def __init__(self, use_local_uri: bool = False):
        super().__init__(use_local_uri)

    def run(self) -> None:
        """
        Executes the scraping process to retrieve the main offer data from the Mercado Livre website.
        The scraped data is then stored in a MongoDB collection if it is a new offer.
        """
        soup = BeautifulSoup(
            requests.get("https://www.mercadolivre.com.br/").text, "html.parser"
        )
        data = {}

        for key, selector in self.selectors.items():
            element = soup.select_one(selector)
            try:
                data[key] = element.text.strip()
            except AttributeError:
                logging.error(f"Error scraping {key}")
                break

        self.write(data)

    @property
    def collection_name(self) -> str:
        return "main_offers"

    @property
    def selectors(self) -> dict[str, str]:
        return dict(
            offer_title=r"#\:Raidq\: > div.andes-carousel-snapped__controls-wrapper > div > div > div > div > "
            "div.poly-card__content > a",
            original_price=r"#\:Raidq\: > div.andes-carousel-snapped__controls-wrapper > div > div > div > div > "
            "div.poly-card__content > div.poly-component__price > s",
            current_price=r"#\:Raidq\: > div.andes-carousel-snapped__controls-wrapper > div > div > div > div > "
            "div.poly-card__content > div.poly-component__price > div > "
            "span.andes-money-amount.andes-money-amount--cents-superscript",
            amount_discount=r"#\:Raidq\: > div.andes-carousel-snapped__controls-wrapper > div > div > div > div > "
            "div.poly-card__content > div.poly-component__price > div > span.andes-money-amount__discount",
            installments=r"#\:Raidq\: > div.andes-carousel-snapped__controls-wrapper > div > div > div > div > "
            "div.poly-card__content > div.poly-component__price > span",
            shipping=r"#\:Raidq\: > div.andes-carousel-snapped__controls-wrapper > div > div > div > div > "
            "div.poly-card__content > div.poly-component__shipping",
        )


if __name__ == "__main__":
    task = Task(use_local_uri=True)
    task.run()
    task.read()
