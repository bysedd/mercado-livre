import json
from datetime import datetime
from time import sleep

from botasaurus import *
from bson import json_util
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from scripts.const import SELECTORS


def get_client() -> MongoClient:
    uri = (
        "mongodb+srv://4drade:ws4vQVUziI3fvBan@cluster0.dwjmome.mongodb.net/?retryWrites=true&w=majority&appName"
        "=Cluster0"
    )
    client = MongoClient(uri, server_api=ServerApi("1"))
    try:
        return client
    except Exception as e:
        print(e)


class Task:
    collection_name = "offers_collection"

    def __init__(self) -> None:
        self.__request = bt.create_requests()
        self.__client = get_client()

    def scrape_main_offer(self) -> None:
        soup = self.__request.bs4("https://www.mercadolivre.com.br/")

        data = {}
        max_attempts = 10
        time_interval = 1

        for key in SELECTORS:
            for i in range(max_attempts):
                element = soup.select_one(SELECTORS[key])
                if element and element.text:
                    data[key] = element.text.strip()
                    break
                elif i != (max_attempts - 1):
                    sleep(time_interval)
                else:
                    data[key] = "Attribute not found"

        self.__write(data=data)

    def __write(self, data: dict) -> None:
        print("Writing")
        print("\t" + self.collection_name)

        client = self.__client
        db = client["mercado_livre"]
        collection = db[self.collection_name]

        new_offer = {
            "datetime": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "main_offer": data,
        }

        if collection.find_one({"main_offer": new_offer["main_offer"]}) is None:
            collection.insert_one(new_offer)

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
