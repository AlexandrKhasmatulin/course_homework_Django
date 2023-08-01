from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    email = models.EmailField(verbose_name="Контактный email", unique=True,)
    client = models.CharField(max_length=100, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", **NULLABLE)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.id} - {self.client}"


class Mailing(models.Model):
    title = models.CharField(max_length=100, verbose_name="Тема письма", **NULLABLE)
    content = models.TextField(verbose_name='Содержимое письма', **NULLABLE)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"{self.title}"


class SmsLetter(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент", related_name='sms_letters')
    title = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")
    send_time = models.TimeField(default=timezone.now(), verbose_name="Время рассылки")
    frequency = models.CharField(default="", max_length=10,
                                 choices=[("day", "Раз в день"), ("week", "Раз в неделю"), ("month", "Раз в месяц")],
                                 verbose_name="Периодичность")
    status = models.CharField(max_length=10,
                              choices=[("created", "Создана"), ("started", "Запущена"), ("finished", "Завершена")],
                              verbose_name="Статус рассылки", default="Создание")
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('smslatter_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Смс рассылка"
        verbose_name_plural = "Смс рассылки"

    def __str__(self):
        return f"{self.title} {self.client}"


class MailingLog(models.Model):
    send_time = models.ForeignKey(SmsLetter, on_delete=models.CASCADE, verbose_name="время рассылки")
    status = models.CharField(max_length=10, choices=[("success", "Успешно"), ("failed", "Неудачно")],
                              verbose_name="Статус попытки",null=False)
    server_response = models.TextField(verbose_name="Ответ почтового сервера, если он был")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")

    class Meta:
        verbose_name = "Лог"
        verbose_name_plural = "Логи"

    def __str__(self):
        return f"{self.status} {self.send_time} "

