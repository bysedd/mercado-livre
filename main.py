import json
import re

from botasaurus import *

file_name = "scrape_main_offer"


@request(
    cache=True,
    output=file_name,
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

    main_offer = soup.find(
        "div", {"class": "ui-recommendations-carousel-snapped new-carousel"}
    ).get_text()

    main_offer = main_offer.replace("Oferta do dia", "")  # Removing 'Oferta do dia'

    parsed_info = re.search(
        r"^(.*?) - (.*?)(R\$(?:\d+\.)*\d+)(R\$(?:\d+\.)*\d{3})(\d+% OFF)(.*?juros)(.*)$",
        main_offer,
    )

    if parsed_info:
        offer_text = parsed_info.group(1) + " - " + parsed_info.group(2)
        offer_text = offer_text.replace('"', "")  # Removing the double quotes

        main_offer = {
            "offer_text": offer_text,
            "original_price": parsed_info.group(3),
            "discount_price": parsed_info.group(4),
            "discount_percentage": parsed_info.group(5),
            "installment_details": parsed_info.group(6),
            "extra_info": parsed_info.group(7),
        }
    else:
        print("The text does not match the expected format.")

    # Save the data as a JSON file in output/*.json
    return {"main_offer": main_offer}


def read_main_offer() -> None:
    """
    Reads the main offer from a JSON file and prints it with indentation.
    """
    print("Reading")
    print(json.dumps(bt.read_json(file_name)[0], indent=4, ensure_ascii=False))


if __name__ == "__main__":
    scrape_main_offer_task()
    read_main_offer()
