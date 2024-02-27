from scripts.utils import BaseTask


class Task(BaseTask):
    """
    The Task class represents a task object for handling tasks related to a specific collection of other offers.
    """

    def __init__(self, use_local_uri: bool = False):
        super().__init__(use_local_uri)

    def get_soup_selector(self) -> str:
        return "div.poly-card poly-card--grid"

    @property
    def collection_name(self) -> str:
        return "other_offers"


if __name__ == "__main__":
    task = Task(use_local_uri=True)
    task.run()
    task.read()
