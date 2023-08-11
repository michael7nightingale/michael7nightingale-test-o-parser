from celery import shared_task
from datetime import datetime
from django.conf import settings

from services.parser.main import OzoneProductsParser
from services.telegram.messages import send_message
from products.models import Product, ParseTask


@shared_task()
def parse_products_task(n: int, chat_id) -> None:
    """Main task to start products parsing."""
    parse_task = ParseTask.objects.create(
        n_pages=n,
        chat_id=chat_id
    )
    with OzoneProductsParser(base_url="https://www.ozon.ru/seller/proffi-1/products", max_pages=n) as parser:
        try:
            result = parser()
            saved = 0
            for goods_page in result:
                for good in goods_page:
                    try:
                        Product.objects.get_or_create(**good, parse_task=parse_task)
                        saved += 1
                    except:
                        continue
            parse_task.success = True
            parse_task.time_finished = datetime.now()
            parse_task.save()
            message = f"Parse task id={parse_task.id} is finished successfully. Saved {saved} products."
        except Exception as e:
            message = f"Parser task id={parse_task.id} is finished with error: {str(e)}"

    send_message(
        message=message,
        token=settings.TOKEN,
        chat_id=chat_id
    )
