from bs4.element import Tag

from scripts.utils import BaseTask


class Task(BaseTask):
    def __init__(self, use_local_uri: bool = False):
        super().__init__(use_local_uri)

    def get_soup_selector(self, soup) -> Tag:
        return soup.select_one("div.ui-recommendations-carousel-snapped.new-carousel")

    @property
    def collection_name(self) -> str:
        return "main_offers"


if __name__ == "__main__":
    task = Task(use_local_uri=True)
    task.run()
    task.read()
