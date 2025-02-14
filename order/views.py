from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import permissions, viewsets

from .models import Category, Product, Receipt
from .serializers import CategoryProductsSerializer, CategorySerializer, ProductSerializer, ReceiptSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReceiptViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows receipts to be viewed and updated.
    """
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows second-level categories to be viewed.
    """
    queryset = Category.objects.filter(
        parent__parent__isnull=True).exclude(
            parent=None).order_by('parent')
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryProductsSerializer
        return CategorySerializer
