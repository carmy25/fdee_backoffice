from order import views
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
