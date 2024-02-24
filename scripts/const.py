SELECTORS = dict(
    offer_title=r"#\:Raidq\: > div.andes-carousel-snapped__controls-wrapper > div > div > div > div > "
    "div.poly-card__content > a",
    original_price=r"#\:Raidq\: > div.andes-carousel-snapped__controls-wrapper > div > div > div > div > "
    "div.poly-card__content > div.poly-component__price > s",
    current_price=r"#\:Raidq\: > div.andes-carousel-snapped__controls-wrapper > div > div > div > div > "
    "div.poly-card__content > div.poly-component__price > div > "
    "span.andes-money-amount.andes-money-amount--cents-superscript",
    amount_discount=r"#\:Raidq\: > div.andes-carousel-snapped__controls-wrapper > div > div > div > div > "
    "div.poly-card__content > div.poly-component__price > div > span.andes-money-amount__discount",
    installments=r"#\:Raidq\: > div.andes-carousel-snapped__controls-wrapper > div > div > div > div > "
    "div.poly-card__content > div.poly-component__price > span",
    shipping=r"#\:Raidq\: > div.andes-carousel-snapped__controls-wrapper > div > div > div > div > "
    "div.poly-card__content > div.poly-component__shipping",
)
