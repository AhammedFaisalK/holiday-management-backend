from django.contrib import admin
from .models import HolidayCache

@admin.register(HolidayCache)
class HolidayCacheAdmin(admin.ModelAdmin):
    list_display = ('country_code', 'year', 'created_at', 'updated_at')
    search_fields = ('country_code', 'year')
    list_filter = ('year', 'country_code')
    readonly_fields = ('created_at', 'updated_at')