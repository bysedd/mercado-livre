from bs4.element import ResultSet

from scripts.utils import BaseTask


class Task(BaseTask):
    def __init__(self, use_local_uri: bool = False):
        super().__init__(use_local_uri)

    def get_soup_selector(self, soup) -> ResultSet:
        return soup.find_all("div", class_="poly-card poly-card--grid")

    @property
    def collection_name(self) -> str:
        return "other_offers"


if __name__ == "__main__":
    task = Task(use_local_uri=True)
    task.run()
    task.read()
