from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Notebook, NotebookImg, Card, CardImg, CardVariant


@admin.register(Notebook)
class NotebookAdmin(SortableAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", "code",)}
    list_display = ("name", "size", "price", "code",)
    list_filter = ("name", "size", "price",)

@admin.register(Card)
class CardAdmin(SortableAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", "code",)}
    list_display = ("name", "code", "size", "price", "card_type")
    list_filter = ("size", "price", "in_store", "has_variants", "card_type")    

@admin.register(CardVariant)
class CardVariantAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("card", "variant_name",)
    list_filter = ("card",)  

admin.site.register(NotebookImg)
admin.site.register(CardImg)