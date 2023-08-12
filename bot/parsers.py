from typing import Generator
import csv
from tempfile import TemporaryFile


def parse_products_list(products_list: list[dict], chat_id: str) -> str:
    """Get string response function of the list of products json response."""
    if not products_list:
        return "There is not parsed products."

    def get_strings_raw_gen() -> Generator[str, None, None]:
        for number, product in enumerate(products_list, 1):
            product_string = (
                f"{number}) {product['name']}"
                f"(price: {product['price']} RUB, discount: {product['discount']}%)"
                f"https://www.ozon.ru{product['url']}"
            )
            yield product_string

            if number >= 4:
                message_text = (
                    f"Sorry, list is too long. You can watch it here: http://localhost:8000/api/v1/products?chat={chat_id}"
                )
                yield message_text
                return

    return "\n\n".join(get_strings_raw_gen())


def parse_product(product: dict) -> str:
    """Get string message response"""
    if product:
        return (
            f"ID: {product['id']}\n"
            f"Title: {product['name']}\n"
            f"Price: {product['price']}\n"
            f"Discount: {product['discount']}\n"
            f"URL: {product['url']}"
        )
    else:
        return "There is not such product."
