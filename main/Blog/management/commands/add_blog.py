from django.core.management.base import BaseCommand

from main.Blog.models import Blog


class Command(BaseCommand):
    def handle(self, *args, **options):
        Blog.objects.all().delete(),


        # fruits = Blog.objects.create(title='фрукты')
        # vegetables = Blog.objects.create(title='овощи')
        # berry = Blog.objects.create(title='ягоды')
        # meet = Blog.objects.create(title='мясо')
        # fish = Blog.objects.create(title='рыба')

        Blog.objects.create(title='банан', body='Желтый', preview="/Банан.png")
        Blog.objects.create(title='помидор', body='Красный', preview='/Помидор.png')
        Blog.objects.create(title='орех', body='Коричневый',  preview='/Орех.png')
        Blog.objects.create(title='баранина', body='Кровавая', preview='/Баранина.png')
        Blog.objects.create(title='курица', body='Пернатая', preview='/Курица.png')
        Blog.objects.create(title='килька', body='Скользкая', preview='/Рыба.png')
        Blog.objects.create(title='черешня', body='Красненькая', preview='/Черешня.png')
        Blog.objects.create(title='клубника', body='Розовая', preview='/Клубника.png')






