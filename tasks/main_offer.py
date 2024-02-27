from scripts.utils import BaseTask


class Task(BaseTask):
    """
    A class that represents a task to scrape data from the Mercado Livre website and store it in a MongoDB collection.
    """

    def __init__(self, use_local_uri: bool = False):
        super().__init__(use_local_uri)

    def get_soup_selector(self) -> str:
        return "div.ui-recommendations-carousel-snapped.new-carousel"

    @property
    def collection_name(self) -> str:
        return "main_offers"


if __name__ == "__main__":
    task = Task(use_local_uri=True)
    task.run()
    task.read()
