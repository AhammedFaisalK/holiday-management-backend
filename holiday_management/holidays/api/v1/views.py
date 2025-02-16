from rest_framework import views, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from holidays.services.calendrific import CalendarificService
from .serializers import HolidaySerializer, HolidayRequestSerializer
from holidays.pagination import CustomPagination
import logging

logger = logging.getLogger(__name__)

class HolidayView(views.APIView):
    """View to handle holiday-related requests"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CalendarificService()
        self.paginator = CustomPagination()  

    def get(self, request):
        """Get holidays based on query parameters"""
        serializer = HolidayRequestSerializer(data=request.GET)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            country_code = serializer.validated_data['country_code']
            year = serializer.validated_data['year']
            month = serializer.validated_data.get('month')
            query = serializer.validated_data.get('query', '')
            holiday_type = serializer.validated_data.get('holiday_type', '')

            holidays = self.service.get_holidays(country_code, year)

            if month:
                holidays = self.service.filter_holidays_by_month(country_code, year, month)
            if query:
                holidays = self.service.search_holidays(country_code, year, query)
            if holiday_type:
                holidays = self.service.filter_holidays_by_type(country_code, year, holiday_type)

            # Paginate results
            paginated_holidays = self.paginator.paginate_queryset(holidays, request)
            return self.paginator.get_paginated_response(HolidaySerializer(paginated_holidays, many=True).data)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error processing holiday request: {str(e)}")
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)