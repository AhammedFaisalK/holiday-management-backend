from django.urls import path
from .views import HolidayView

app_name = "api_v1_holidays"

urlpatterns = [
    path('', HolidayView.as_view(), name='holidays'),
]