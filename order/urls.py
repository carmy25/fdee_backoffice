from order import views
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'products', views.ProductViewSet)
router.register(r'receipts', views.ReceiptViewSet)
router.register(r'categories', views.CategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
