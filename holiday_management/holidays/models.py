from django.db import models

class HolidayCache(models.Model):
    country_code = models.CharField(max_length=2)
    year = models.IntegerField()
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'holiday_cache'  
        verbose_name = 'Holiday Cache'
        verbose_name_plural = 'Holiday Caches'
        unique_together = ('country_code', 'year')
        indexes = [
            models.Index(fields=['country_code', 'year'], name='holiday_country_year_idx'),
        ]

    def __str__(self):
        return f"{self.country_code} - {self.year}"