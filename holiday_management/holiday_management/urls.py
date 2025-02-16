from django.contrib import admin
from django.urls import path, include
from holidays.api.v1 import urls as holiday_api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/holidays/', include(holiday_api_urls, namespace="api_v1_holidays")),
]
