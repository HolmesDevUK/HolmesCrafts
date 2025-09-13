from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "name", "role", "is_active", "is_staff")
    list_filter = ("role", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields":("name", "role")}),
        ("Permissions", {"fields":("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields":("last_login", )}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "role", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("email", "name")
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)