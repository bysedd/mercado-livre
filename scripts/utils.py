import json
import logging
import os
import re
from abc import ABC, abstractmethod
from datetime import datetime

import bs4
import requests
from bs4 import BeautifulSoup
from bson import json_util
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class BaseTask(ABC):
    """
    Abstract base class that provides a basic structure for tasks related to scraping data
    from the Mercado Livre website and storing it in a MongoDB database
    """

    def __init__(self, use_local_uri: bool = False):
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
        )
        load_dotenv()
        self.__client = self.__get_client(use_local_uri)
        self.__collection = self.__client["mercado_livre"][self.collection_name]

    @staticmethod
    def __extract_data(element, key, selector) -> str | None:
        try:
            if key == "picture":
                return element["data-src"]
            else:
                return element.text.strip()
        except AttributeError:
            return None

    @staticmethod
    def __normalize_price(price: str) -> int:
        if price:
            regex = re.compile(r"[-+]?\d*\.?\d+")
            match = regex.search(price)
            if match:
                return int(match.group(0).replace(".", "").replace(",", ""))

    def __scrape_data(self):
        """
        Scrapes data from a web page.

        :return: A generator that yields dictionaries containing scraped data.
        :rtype: generator
        """
        soup = BeautifulSoup(requests.get(self.site_url).text, "html.parser")
        offer_card = self.get_soup_selector(soup)

        def scrape_single_card(card: bs4.element.ResultSet | bs4.element.Tag):
            data = {}
            numeric_keys = ["price", "price_current", "amount_discount"]
            for key, selector in self.selectors.items():
                element = card.select_one(selector)
                element = self.__extract_data(element, key, selector)
                data[key] = self.__normalize_price(element) if key in numeric_keys else element
            return data

        if isinstance(offer_card, bs4.element.Tag):
            logging.info("Scraping main offers")
            yield scrape_single_card(offer_card)
        elif isinstance(offer_card, bs4.element.ResultSet):
            logging.info("Scraping other offers")
            for card in offer_card:
                yield scrape_single_card(card)

    def run(self) -> None:
        for data in self.__scrape_data():
            self.__write(data)

    @staticmethod
    def __get_client(use_local_uri: bool = False) -> MongoClient:
        """
        Get a MongoClient object for connecting to a MongoDB database.

        :param use_local_uri: A boolean flag indicating whether to use the local URI or the environment URI.
        :return: A MongoClient object.
        """
        uri = os.getenv("URI") if use_local_uri else os.environ["URI"]
        client = MongoClient(uri, server_api=ServerApi("1"))
        return client

    def __write(self, data: dict) -> None:
        """
        Write method for inserting data into the database.

        :param data: A dictionary containing the data to be inserted.
        """
        new_offer = {
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        }
        new_offer.update(data)

        find_offer = {k: v for k, v in new_offer.items() if k in self.selectors.keys()}
        existing_offer = self.__collection.find_one(find_offer)

        if existing_offer is None:
            self.__collection.insert_one(new_offer)
            logging.info("New offer inserted to collection.")
        else:
            logging.info("Offer already exists in collection.")

    def read(self) -> None:
        """
        Read a random offer from the collection.
        """
        print("Reading random offer")
        # Get a random offer from the collection
        random_offer = self.__collection.aggregate([{"$sample": {"size": 1}}])
        # Extract the offer document
        random_offer_doc = next(random_offer, None)

        # Print the offer document
        if random_offer_doc is not None:
            print(
                json.dumps(
                    random_offer_doc,
                    default=json_util.default,
                    indent=4,
                    ensure_ascii=False,
                )
            )
        else:
            logging.error("No offer found in the collection")

    @property
    @abstractmethod
    def collection_name(self) -> str:
        pass

    @abstractmethod
    def get_soup_selector(
        self, soup: BeautifulSoup
    ) -> bs4.element.Tag | bs4.element.ResultSet:
        pass

    @property
    def selectors(self) -> dict[str, str]:
        return dict(
            picture="img.poly-component__picture.poly-component__picture--square",
            title="a.poly-component__title",
            price="s.andes-money-amount.andes-money-amount--previous.andes-money-amount--cents-comma",
            price_current="span.andes-money-amount.andes-money-amount--cents-superscript",
            amount_discount="span.andes-money-amount__discount",
            installments="span.poly-price__installments.poly-text-positive",
            shipping="div.poly-component__shipping",
        )

    @property
    def site_url(self) -> str:
        return "https://www.mercadolivre.com.br/"
