from django.db import models

NULLABLE = {"blank": True, "null": True}
ABLE = {"blank": False, "null": False}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    slug = models.CharField(max_length=150, verbose_name="Slug", **NULLABLE)
    body = models.TextField(verbose_name="Содержимое", **NULLABLE)
    preview = models.ImageField(upload_to='media/', verbose_name="Фото", **NULLABLE)
    create_data = models.DateField(default='2023-06-20', verbose_name="Дата создания", **NULLABLE)
    sign_publication = models.CharField(max_length=150, verbose_name="Признак публикации", **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'