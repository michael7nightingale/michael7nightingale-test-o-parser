import requests
import os


Response = tuple[int, str | dict | list]

# base url to send requests
host_url = os.getenv("HOST_URL")


def get_url(url: str) -> str:
    """Build url function using base host url."""
    return host_url + url


def post_new_chat(chat_id: str) -> Response:
    data = {
        "id": chat_id
    }
    response = requests.post(get_url("chats/"), json=data)
    return response.status_code, response.json()


def get_products(chat_id: str) -> Response:
    response = requests.get(get_url(f"products?chat={chat_id}"))
    return response.status_code, response.json()


def post_run_task(n: int, chat_id: str) -> Response:
    data = {
        "n": n,
        "chat_id": chat_id
    }
    response = requests.post(get_url("products/"), json=data)
    return response.status_code, response.json()


def get_product(product_id: str, chat_id: str) -> Response:
    response = requests.get(get_url(f"products/{product_id}/"))
    return response.status_code, response.json()
