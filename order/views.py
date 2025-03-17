from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response

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
    serializer_class = ReceiptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Receipt.objects.all()

    def list(self, request):
        queryset = Receipt.objects.actual()
        serializer = ReceiptSerializer(queryset, many=True)
        return Response(serializer.data)


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
