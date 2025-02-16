from rest_framework import serializers

class HolidaySerializer(serializers.Serializer):
    """Serializer for holiday data"""
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True, allow_blank=True)
    date = serializers.DictField()
    type = serializers.ListField(child=serializers.CharField())
    locations = serializers.CharField(allow_null=True)
    states = serializers.CharField(allow_null=True)

class HolidayRequestSerializer(serializers.Serializer):
    """Serializer for holiday request parameters"""
    country_code = serializers.CharField(max_length=2)
    year = serializers.IntegerField(min_value=1900, max_value=2099)
    month = serializers.IntegerField(min_value=1, max_value=12, required=False)
    query = serializers.CharField(required=False, allow_blank=True)
    holiday_type = serializers.CharField(required=False, allow_blank=True)