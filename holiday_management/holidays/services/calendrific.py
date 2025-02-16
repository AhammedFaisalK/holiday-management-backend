import requests
from django.conf import settings
from django.core.cache import cache
from ..models import HolidayCache
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class CalendarificService:
    """Service class to handle interactions with the Calendarific API"""
    
    def __init__(self):
        self.api_key = settings.CALENDARIFIC_API_KEY
        self.base_url = settings.CALENDARIFIC_BASE_URL
        self.cache_timeout = settings.HOLIDAY_CACHE_TIMEOUT

    def _get_cache_key(self, country_code: str, year: int) -> str:
        """Generate a cache key for holiday data"""
        return f"holidays_{country_code}_{year}"

    def _fetch_from_api(self, country_code: str, year: int) -> dict:
        """Fetch holiday data from Calendarific API"""
        try:
            response = requests.get(
                f"{self.base_url}/holidays",
                params={
                    "api_key": self.api_key,
                    "country": country_code,
                    "year": year,
                }
            )
            response.raise_for_status()
            return response.json().get('response', {}).get('holidays', [])
        except requests.RequestException as e:
            logger.error(f"Error fetching holidays: {str(e)}")
            raise

    def get_holidays(self, country_code: str, year: int) -> list:
        """
        Get holidays for a specific country and year.
        Attempts to fetch from cache first, then falls back to API.
        """
        cache_key = self._get_cache_key(country_code, year)
        
        # Try memory cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        # Try database cache
        try:
            db_cache = HolidayCache.objects.get(country_code=country_code, year=year)
            cache.set(cache_key, db_cache.data, self.cache_timeout)
            return db_cache.data
        except HolidayCache.DoesNotExist:
            pass

        # Fetch from API
        holidays = self._fetch_from_api(country_code, year)
        
        # Update both caches
        cache.set(cache_key, holidays, self.cache_timeout)
        HolidayCache.objects.update_or_create(
            country_code=country_code,
            year=year,
            defaults={'data': holidays}
        )
        
        return holidays

    def search_holidays(self, country_code: str, year: int, query: str) -> list:
        """Search holidays by name"""
        holidays = self.get_holidays(country_code, year)
        query = query.lower()
        return [
            holiday for holiday in holidays
            if query in holiday.get('name', '').lower()
        ]

    def filter_holidays_by_month(self, country_code: str, year: int, month: int) -> list:
        """Filter holidays by month"""
        holidays = self.get_holidays(country_code, year)
        return [
            holiday for holiday in holidays
            if datetime.strptime(holiday.get('date', {}).get('iso'), '%Y-%m-%d').month == month
        ]

    def filter_holidays_by_type(self, country_code: str, year: int, holiday_type: str) -> list:
        """Filter holidays by type"""
        holidays = self.get_holidays(country_code, year)
        return [
            holiday for holiday in holidays
            if holiday_type.lower() in [t.lower() for t in holiday.get('type', [])]
        ]