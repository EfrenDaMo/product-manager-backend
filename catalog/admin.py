from django.contrib import admin
from .models import Category, Product, StockMovement

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "is_active", "created_at")
    list_filter = ("is_active", "parent")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "quantity", "price", "is_active")
    list_filter = ("is_active", "category", "unit")
    search_fields = ("name", "sku", "barcode")
    readonly_fields = ("quantity", "created_at", "updated_at")

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("product", "delta", "reason", "created_by", "created_at")
    list_filter = ("reason",)
    readonly_fields = ("created_at",)
