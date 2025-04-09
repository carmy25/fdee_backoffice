from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from datetime import date
from django.db.models import Sum, Q

from .models import Category, Product, Receipt
from .serializers import CategoryProductsSerializer, CategorySerializer, ProductSerializer, ReceiptSerializer
from .forms import DailyReportDateRange


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
    permission_classes = [permissions.IsAuthenticated]

    queryset = Category.objects.filter(
        parent__isnull=False).order_by('parent')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryProductsSerializer
        return CategorySerializer

    def list(self, request):
        queryset = Category.objects.top_level()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


def calculate_category_totals(receipts, category_name):
    # Get the main category and all its children
    main_category = Category.objects.filter(name=category_name).first()
    if not main_category:
        return {'card': 0, 'cash': 0, 'card_transfer': 0}

    # Get all child categories including the main category
    category_and_children = main_category.collect_children()

    # Filter receipts by products in this category and its children
    def get_total_for_payment_method(payment_method):
        category_receipts = receipts.filter(payment_method=payment_method)
        total = 0
        if payment_method == Receipt.PaymentMethod.CASH:
            if category_name == 'Бар':
                pass
        for receipt in category_receipts:
            for item in receipt.product_items.all():
                if any(cat == item.product_type.category for cat in category_and_children):
                    total += item.total_price()
        return total

    return {
        'card': get_total_for_payment_method(Receipt.PaymentMethod.CARD),
        'cash': get_total_for_payment_method(Receipt.PaymentMethod.CASH),
        'card_transfer': get_total_for_payment_method(Receipt.PaymentMethod.CARD_TRANSFER)
    }


@staff_member_required
def daily_report_admin_page(request):
    start_date = date.today()
    end_date = date.today()
    form = DailyReportDateRange(initial={
        'start_date': start_date,
        'end_date': end_date
    })

    # Get closed receipts
    receipts = Receipt.objects.filter(
        status=Receipt.Status.CLOSED,
        created_at__date__range=(start_date, end_date))

    if request.method == 'POST':
        form = DailyReportDateRange(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            receipts = receipts.filter(
                status=Receipt.Status.CLOSED,
                created_at__date__range=(start_date, end_date))

    # Calculate totals for Bar and Kitchen
    bar_totals = calculate_category_totals(receipts, 'Бар')
    kitchen_totals = calculate_category_totals(receipts, 'Кухня')

    # Calculate overall totals
    overall_totals = {
        'card': bar_totals['card'] + kitchen_totals['card'],
        'cash': bar_totals['cash'] + kitchen_totals['cash'],
        'card_transfer': bar_totals['card_transfer'] + kitchen_totals['card_transfer']
    }

    # Add total for each category
    bar_totals['total'] = bar_totals['card'] + \
        bar_totals['cash'] + bar_totals['card_transfer']
    kitchen_totals['total'] = kitchen_totals['card'] + \
        kitchen_totals['cash'] + kitchen_totals['card_transfer']
    overall_totals['total'] = overall_totals['card'] + \
        overall_totals['cash'] + overall_totals['card_transfer']

    return render(request,
                  "admin/daily_report_admin_page.html",
                  {"title": "Поденний звіт",
                   "site_header": "FOODee Офіс",
                   'date_range_form': form,
                   'bar_totals': bar_totals,
                   'kitchen_totals': kitchen_totals,
                   'overall_totals': overall_totals})
