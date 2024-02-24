from scripts.utils import read_main_offer
from tasks.scrape_offer import scrape_main_offer_task


if __name__ == "__main__":
    scrape_main_offer_task()
    read_main_offer()
