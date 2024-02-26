import json
import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime

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

    @abstractmethod
    def run(self) -> None:
        pass

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
        if len(data.keys()) == 6:
            client = self.__client
            db = client["mercado_livre"]
            collection = db[self.collection_name]
            new_offer = {
                "date_added": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
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

    @property
    @abstractmethod
    def selectors(self) -> dict[str, str]:
        pass
