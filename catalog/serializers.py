from rest_framework import serializers
from .models import Category, Product, StockMovement

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "description", "parent", "slug", "is_active", "created_by", "created_at", "updated_by", "updated_at")
        read_only_fields = ("id", "slug", "created_by", "created_at", "updated_by", "updated_at")

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "brand", "category", "quantity", "price", "sku", "barcode", "unit", "description", "is_active",
                "created_by", "created_at", "updated_by", "updated_at")
        read_only_fields = ("id", "quantity", "created_by", "created_at", "updated_by", "updated_at")

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ("id", "product", "delta", "reason", "created_by", "created_at")
        read_only_fields = ("id", "created_by", "created_at")

    def validate(self, data):
        product = data.get("product") or self.instance.product
        delta = data.get("delta")
        if product and delta is not None and (product.quantity + delta) < 0:
            raise serializers.ValidationError("This movement would result in negative stock.")
        return data

    def create(self, validated_data):
        movement = StockMovement.objects.create(
            **validated_data, created_by=self.context["request"].user
        )
        product = movement.product
        if product:
            product.quantity += movement.delta
            product.save(update_fields=["quantity"])
        return movement
