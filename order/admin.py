from django.contrib import admin
from rangefilter.filters import DateRangeFilterBuilder

from order.models import Category, Product, ProductItem, Receipt


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['full_name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


class ProductItemInline(admin.TabularInline):
    model = ProductItem
    extra = 0
    verbose_name = 'товар'
    verbose_name_plural = 'товари'
    fields = ('product_type', 'amount')
    readonly_fields = (
        'product_type',
        'amount',
    )
    can_delete = False

    def has_add_permission(self, request, obj):
        return False


class ReceiptAdmin(admin.ModelAdmin):
    inlines = (ProductItemInline,)
    ordering = ['-created_at']
    exclude = ('updated_at',)
    list_display = (
        'id', 'status', 'place', 'created_at', 'updated_at',
        'payment_method', 'price',
    )
    list_filter = (
        ("created_at", DateRangeFilterBuilder()),
    )

    def has_add_permission(self, request):
        return False


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Receipt, ReceiptAdmin)
