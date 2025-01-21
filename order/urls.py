from order import views
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'receipts', views.ReceiptViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
