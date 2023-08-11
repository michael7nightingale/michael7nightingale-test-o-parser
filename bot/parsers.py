from typing import Generator


def parse_products_list(products_list: list[dict]) -> str:

    def get_strings_raw_gen() -> Generator[str, None, None]:
        for number, product in enumerate(products_list, 1):
            product_string = (
                f"{number}) {product['title']}"
                f"(price: {product['price']} RUB, discount: {product['discount']}%)"
                f"https://www.ozon.ru{product['url']}"
            )
            yield product_string

            if number >= 4:
                message_text = (
                    f"Sorry, list is too long. You can watch it here: http://localhost:8000/api/v1/products/"
                    "\nor type /download to get .csv file."
                )
                yield message_text
                return

    return "\n\n".join(get_strings_raw_gen())


def parse_product(product: dict) -> str:
    return (
        f"ID: {product['id']}\n"
        f"Title: {product['title']}\n"
        f"Price: {product['price']}\n"
        f"Discount: {product['discount']}\n"
        f"URL: {product['url']}"
    )
