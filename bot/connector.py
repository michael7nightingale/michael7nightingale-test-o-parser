import requests
import os


host_url = os.getenv("HOST_URL")


def get_url(url: str) -> str:
    return host_url + url


def post_new_chat(chat_id: str):
    data = {
        "id": "chat_id"
    }
    response = requests.post(get_url("chats/"), json=data)
    return response


def get_products() -> list:
    response = requests.get(get_url("products"))
    return response.json()


def post_run_task(n: int) -> list:
    response = requests.get(get_url("products"))
    return response.json()


def get_product(product_id: str) -> list:
    response = requests.get(get_url(f"products/{product_id}/"))
    return response.json()
