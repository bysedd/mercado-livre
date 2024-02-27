import json
import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from bson import json_util
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class BaseTask(ABC):
    def __init__(self, use_local_uri: bool = False):
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
        )
        load_dotenv()
        self.__client = self.get_client(use_local_uri)

    def scrape_data(self, soup_selector: str) -> dict:
        soup = BeautifulSoup(
            requests.get("https://www.mercadolivre.com.br/").text, "html.parser"
        )
        data = {}
        offer_card = soup.select(soup_selector)

        for card in offer_card:
            for key, selector in self.selectors.items():
                element = card.select_one(selector)
                try:
                    if key == "picture":
                        data[key] = element["data-src"]
                    else:
                        data[key] = element.text.strip()
                except AttributeError:
                    data[key] = None
        return data

    def run(self) -> None:
        self.write(self.scrape_data(self.get_soup_selector()))

    @staticmethod
    def get_client(use_local_uri: bool = False) -> MongoClient:
        """
        Get a MongoClient object for connecting to a MongoDB database.

        :param use_local_uri: A boolean flag indicating whether to use the local URI or the environment URI.
        :return: A MongoClient object.
        """
        uri = os.getenv("URI") if use_local_uri else os.environ["URI"]
        client = MongoClient(uri, server_api=ServerApi("1"))
        return client

    def write(self, data: dict) -> None:
        """
        Write method for inserting data into the database.

        :param data: A dictionary containing the data to be inserted.
        """
        client = self.__client
        db = client["mercado_livre"]
        collection = db[self.collection_name]
        new_offer = {
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "offer": data,
        }

        if collection.find_one({"offer": new_offer["offer"]}) is None:
            collection.insert_one(new_offer)
            logging.info("New offer inserted")
        else:
            logging.info("Offer already exists")

    def read(self) -> None:
        """
        Read a random offer from the collection.
        """
        print("Reading random offer")
        client = self.__client
        db = client["mercado_livre"]
        collection = db[self.collection_name]
        # Get a random offer from the collection
        random_offer = collection.aggregate([{"$sample": {"size": 1}}])
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
    def get_soup_selector(self) -> str:
        pass

    @property
    def selectors(self) -> dict[str, str]:
        return dict(
            picture="img.poly-component__picture.poly-component__picture--square",
            title="a.poly-component__title",
            previous_price="s.andes-money-amount.andes-money-amount--previous.andes-money-amount--cents-comma",
            current_price="pan.andes-money-amount.andes-money-amount--cents-superscript",
            amount_discount="span.andes-money-amount__discount",
            installments="span.poly-price__installments.poly-text-positive",
            shipping="div.poly-component__shipping",
        )
