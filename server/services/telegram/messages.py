import requests


def send_message(message: str, token: str, chat_id: str) -> None:
    """Send message using Telegram API."""
    send_text = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}'
    response = requests.get(send_text)
    print(response.json())
