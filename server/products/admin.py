from django.contrib import admin

from .models import ParseTask, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name_preview", "parse_task")
    search_fields = ("name", )
    list_display_links = ("id", "name_preview")


@admin.register(ParseTask)
class ParseTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "chat", "time_created", "success")
    search_fields = ("success", )
    list_display_links = ("id", "time_created")
