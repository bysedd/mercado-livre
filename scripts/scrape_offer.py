import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from bson import json_util
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import logging
import os

from scripts.const import SELECTORS

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(message)s", datefmt="%d-%m-%Y %H:%M:%S"
)


def get_client() -> MongoClient:
    uri = os.environ['URI']
    client = MongoClient(uri, server_api=ServerApi("1"))
    try:
        return client
    except Exception as e:
        print(e)


class Task:
    collection_name = "offers_collection"

    def __init__(self) -> None:
        self.__client = get_client()

    def scrape_main_offer(self) -> None:
        soup = BeautifulSoup(
            requests.get("https://www.mercadolivre.com.br/").text, "html.parser"
        )
        data: dict[str, str] = {}

        for key, selector in SELECTORS.items():
            element = soup.select_one(selector)
            if element and element.text:
                data[key] = element.text.strip()
            else:
                data[key] = "Attribute not found"

        self.__write(data=data)

    def __write(self, data: dict) -> None:
        client = self.__client
        db = client["mercado_livre"]
        collection = db[self.collection_name]

        new_offer = {
            "datetime": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "main_offer": data,
        }

        if collection.find_one({"main_offer": new_offer["main_offer"]}) is None:
            collection.insert_one(new_offer)
            logging.info("New offer inserted")
        else:
            logging.info("Offer already exists")

    def read(self) -> None:
        print("Reading last offer")

        client = self.__client
        db = client["mercado_livre"]
        collection = db[self.collection_name]
        # Get the last offer from the collection
        last_offer = collection.find().sort([("datetime", -1)]).limit(1)[0]

        # Print the last offer
        print(
            json.dumps(
                last_offer, default=json_util.default, indent=4, ensure_ascii=False
            )
        )
