from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_active", "date_joined")
    list_filter = ("role", "is_staff", "is_active")

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Extra", {"fields": ("role", "created_by", "updated_by")}),
    )
    readonly_fields = ("updated_at",)

admin.site.register(User, UserAdmin)
