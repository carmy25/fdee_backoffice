"""
URL configuration for foodee_backoffice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.http import HttpResponse
from django.urls import include, path
from django.conf.urls.static import static

from django.conf import settings
from foodee_backoffice.admin import admin


def sentry_debug(request):
    # Add some context that Sentry should capture
    from sentry_sdk import set_context
    set_context("test_metadata", {
        "endpoint": "sentry-debug",
        "test_date": "2025-04-26"
    })
    # This will raise a ZeroDivisionError
    return 1 / 0


urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("user/", include('user.urls')),
    path("order/", include('order.urls')),
    path("place/", include('place.urls')),
    path('sentry-debug/', sentry_debug),
    path('ping/', lambda request: HttpResponse('pong')),
]
