from ast import While
from typing import override

from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children"
    )

    slug = models.SlugField(unique=True, null=True)

    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="categories_created"
    )
    created_at = models.DateTimeField(auto_now=True)

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="categories_updated"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"

    @override
    def __str__(self):
        return f"{self.name}"

    @override
    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

class Product(models.Model):
    class Unit(models.TextChoices):
        PIECE = "pcs", "Pieces"
        GRAM = "g", "gram"
        KILOGRAM = "kg", "Kilogram"
        LITER = "l", "Liter"
        MILLILITER = "ml", "Milliliter"
        BOX = "box" "Box"

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True, null=True)

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products"
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)

    sku = models.CharField(max_length=64, unique=True)
    unit = models.CharField(max_length=10, choices=Unit.choices, default=Unit.PIECE)
    barcode = models.CharField(max_length=64, unique=True, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products_updated",
    )
    updated_at = models.DateTimeField(auto_now=True)

    @override
    def __str__(self):
        return f"{self.name}"

class StockMovement(models.Model):
    product = models.ForeignKey(
        Product,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="movements"

    )

    delta = models.IntegerField()
    reason = models.CharField(max_length=255, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="stock_movements_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    @override
    def __str__(self):
        return f"{self.product} ({self.delta:+d})"
