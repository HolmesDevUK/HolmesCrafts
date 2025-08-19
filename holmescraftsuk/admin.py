from django.contrib import admin

from .models import Notebook, NotebookImg, Card, CardImg, CardVariant, Navbar
# Register your models here.

class NotebookAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", "code",)}
    list_display = ("name", "size", "price", "code",)
    list_filter = ("name", "size", "price",)

class CardAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", "code",)}
    list_display = ("name", "code", "size", "price", "card_type")
    list_filter = ("size", "price", "in_store", "has_variants", "card_type")    

class CardVariantAdmin(admin.ModelAdmin):
    list_display = ("card", "variant_name",)
    list_filter = ("card",)

class NavbarAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("page_name",)}
    list_display = ("page_name", "url", "slug")    

admin.site.register(Notebook, NotebookAdmin)
admin.site.register(NotebookImg)
admin.site.register(Card, CardAdmin)
admin.site.register(CardImg,)
admin.site.register(CardVariant, CardVariantAdmin)
admin.site.register(Navbar, NavbarAdmin)
