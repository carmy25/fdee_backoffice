from order import views
from django.urls import path, include
from rest_framework import routers
from .views import daily_report_admin_page

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'products', views.ProductViewSet)
router.register(r'receipts', views.ReceiptViewSet, basename='receipt')
router.register(r'categories', views.CategoryViewSet, basename='category')


urlpatterns = [
    path('', include(router.urls)),
    path("admin/dayly-report/", daily_report_admin_page,
         name="daily_report_admin_page"),
]
