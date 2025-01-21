from django.contrib import admin

from order.models import Category, Product, Receipt


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['full_name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


class ReceiptAdmin(admin.ModelAdmin):
    ordering = ['created_at']
    exclude = ('updated_at',)
    list_display = ['number', 'place', 'created_at', 'updated_at']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Receipt, ReceiptAdmin)
