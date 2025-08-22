from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Product, Notebook, NotebookImg, Card, CardImg, CardVariant, Size, PriceGroup, Tag, ProductType, CardInsert, CardType

@admin.register(Product)
class ProductAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "size", "price_group", "code", "is_featured", "in_store",)
    filter_horizontal = ("tags",)


@admin.register(Notebook)
class NotebookAdmin(SortableAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", "code",)}
    list_display = ("name", "code",)
    list_filter = ("name",)

@admin.register(Card)
class CardAdmin(SortableAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", "code",)}
    list_display = ("name", "code", "card_type")
    list_filter = ("in_store", "has_variants", "card_type")    

@admin.register(CardVariant)
class CardVariantAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("card", "variant_name",)
    list_filter = ("card",)   

@admin.register(Size)
class SizeAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "orientation",)
    list_filter = ("name", "orientation",)

@admin.register(PriceGroup)
class PriceGroupAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("product_type", "size", "price",)
    list_filter =  ("product_type", "size", "price",)

admin.site.register(NotebookImg)
admin.site.register(CardImg)
admin.site.register(Tag)
admin.site.register(CardType)
admin.site.register(CardInsert)
admin.site.register(ProductType)