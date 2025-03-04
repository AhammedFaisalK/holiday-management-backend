# Generated by Django 5.0.2 on 2025-02-16 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HolidayCache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(max_length=2)),
                ('year', models.IntegerField()),
                ('data', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Holiday Cache',
                'verbose_name_plural': 'Holiday Caches',
                'db_table': 'holiday_cache',
                'indexes': [models.Index(fields=['country_code', 'year'], name='holiday_country_year_idx')],
                'unique_together': {('country_code', 'year')},
            },
        ),
    ]
