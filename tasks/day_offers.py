import requests
from bs4 import BeautifulSoup

from scripts.utils import BaseTask


class Task(BaseTask):
    def __init__(self, use_local_uri: bool = False):
        super().__init__(use_local_uri)

    def run(self) -> None:
        """
        Scrapes data from the Mercado Livre website and stores it in a MongoDB collection.
        """
        soup = BeautifulSoup(
            requests.get("https://www.mercadolivre.com.br/").text, "html.parser"
        )
        data = {}
        offer_card = soup.find_all("div", class_="poly-card poly-card--grid")

        for card in offer_card:
            for key, selector in self.selectors.items():
                element = card.select_one(selector)
                data[key] = element.text.strip() if element else None
            self.write(data)

    @property
    def collection_name(self) -> str:
        return "other_offers"

    @property
    def selectors(self) -> dict[str, str]:
        return {
            "title": "a.poly-component__title",
            "previous_price": "s.andes-money-amount.andes-money-amount--previous.andes-money-amount--cents-comma",
            "current_price": "span.andes-money-amount.andes-money-amount--cents-superscript",
            "amount_discount": "span.andes-money-amount__discount",
            "installments": "span.poly-price__installments.poly-text-positive",
            "shipping": "div.poly-component__shipping",
        }


if __name__ == "__main__":
    task = Task(use_local_uri=True)
    task.run()
    task.read()
