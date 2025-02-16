from django.urls import path
from .views import HolidayView

urlpatterns = [
    path('holidays/', HolidayView.as_view(), name='holidays'),
]