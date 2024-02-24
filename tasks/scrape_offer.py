import os
from pathlib import Path
from time import sleep

from botasaurus import *
from dotenv import load_dotenv

from scripts.const import SELECTORS
from scripts.utils import write_file

load_dotenv()

file_name = Path(os.getenv("FILENAME"))
output_dir = Path("output")


@request(
    output=None,
    data=["https://www.mercadolivre.com.br/"],
)
def scrape_main_offer_task(request: AntiDetectRequests, data: list[str]):
    """
    Scrape the main offer from a webpage and return the result as a dictionary.

    :param request: Instance of AntiDetectRequests.
    :param data: List of URLs to scrape.
    :return: Dictionary with the main offers details.
    """
    soup = request.bs4(data)

    data = {}
    max_attempts = 10
    time_interval = 2  # seconds

    for key in SELECTORS:
        for i in range(max_attempts):
            element = soup.select_one(SELECTORS[key])
            if element and element.text:
                data[key] = element.text.strip()
                break
            elif i != (max_attempts - 1):  # Do not sleep after the last attempt
                sleep(time_interval)  # Delay for a specific time interval
            else:
                data[key] = "Attribute not found"  # Or any default value
    
    write_file(data=data, file_path=output_dir / file_name)
