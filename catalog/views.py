from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from .models import Category, Product, StockMovement
from .serializers import CategorySerializer, ProductSerializer, StockMovementSerializer
from accounts.permissions import IsAdmin, IsAuthenticatedOrAdminForDelete


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["parent", "is_active"]
    search_fields = ["name"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrAdminForDelete]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class CategoryBySlugView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

class CategoryToggleActiveView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        category = generics.get_object_or_404(Category, pk=pk)
        category.is_active = not category.is_active
        category.updated_by = request.user
        category.save()
        return Response(CategorySerializer(category).data)

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["category", "is_active", "unit"]
    search_fields = ["name", "sku", "barcode"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrAdminForDelete]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class ProductToggleActiveView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        product = generics.get_object_or_404(Product, pk=pk)
        product.is_active = not product.is_active
        product.updated_by = request.user
        product.save()
        return Response(ProductSerializer(product).data)

class StockMovementListCreateView(generics.ListCreateAPIView):
    serializer_class = StockMovementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["reason"]

    def get_permissions(self):
        return [IsAdmin()] if self.request.method == "GET" else [IsAuthenticated()]

    def get_queryset(self):
        return StockMovement.objects.filter(product_id=self.kwargs["product_id"])

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs["product_id"])
