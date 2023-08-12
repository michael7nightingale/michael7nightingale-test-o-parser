from django.db import models


class ProductManager(models.Manager):
    """Product manager for optimizing SQL orm queries."""
    def get(self, *args, **kwargs):
        return (
            super()
            .select_related("parse_task")
            .get(*args, **kwargs)
        )

    def all(self):
        return (
            super()
            .select_related("parse_task")
            .all()
        )


class Product(models.Model):
    """Product model."""
    id = models.CharField(
        "ID",
        primary_key=True,
        unique=True,
        max_length=255
    )
    url = models.TextField("Product URL")
    image_url = models.TextField("Image URL")
    name = models.CharField("Title", max_length=255)
    price = models.PositiveIntegerField("Price")
    discount = models.PositiveIntegerField("Discount", default=0)
    parse_task = models.ForeignKey("ParseTask", on_delete=models.CASCADE, related_name="products")

    objects = ProductManager()

    @property
    def name_preview(self) -> str:
        return self.name[:30]

    @property
    def total_price(self) -> float:
        return self.price * (1 - (self.discount / 100))  # type: ignore


class ParseTaskManager(models.Manager):
    """Parse task manager for optimizing SQL orm queries."""
    def get(self, *args, **kwargs):
        return (
            super()
            .select_related("chat")
            .prefetch_related("products")
            .get(*args, **kwargs)
        )

    def all(self):
        return (
            super()
            .select_related("chat")
            .prefetch_related("products")
            .all()
        )


class ParseTask(models.Model):
    """Parse task model."""
    chat = models.ForeignKey("chats.Chat", on_delete=models.SET_NULL, null=True, related_name="parse_tasks")
    n_pages = models.PositiveIntegerField("Pages")
    time_created = models.DateTimeField("Time of task creation", auto_now_add=True)
    time_finished = models.DateTimeField("Time task finished", null=True)
    success = models.BooleanField("Success", default=False)

    objects = ParseTaskManager()
