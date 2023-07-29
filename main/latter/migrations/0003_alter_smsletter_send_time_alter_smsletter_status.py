# Generated by Django 4.2.3 on 2023-07-27 12:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('latter', '0002_remove_mailing_client_remove_mailing_frequency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smsletter',
            name='send_time',
            field=models.TimeField(default=datetime.datetime(2023, 7, 27, 12, 8, 6, 416118, tzinfo=datetime.timezone.utc), verbose_name='Время рассылки'),
        ),
        migrations.AlterField(
            model_name='smsletter',
            name='status',
            field=models.CharField(choices=[('created', 'Создана'), ('started', 'Запущена'), ('finished', 'Завершена')], default='Создание', max_length=10, verbose_name='Статус рассылки'),
        ),
    ]