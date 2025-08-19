from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Navbar


@admin.register(Navbar)
class NavbarAdmin(SortableAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("page_name",)}
    list_display = ("page_name", "url", "slug") 