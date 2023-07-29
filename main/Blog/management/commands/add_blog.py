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

        Blog.objects.create(title='банан', body='', preview="/Банан.png")
        Blog.objects.create(title='помидор', body='', preview='/Помидор.png')
        Blog.objects.create(title='орех', body='',  preview='/Орех.png')
        Blog.objects.create(title='баранина', body='', preview='/Баранина.png')
        Blog.objects.create(title='курица', body='', preview='/Курица.png')
        Blog.objects.create(title='килька', body='', preview='/Рыба.png')
        Blog.objects.create(title='черешня', body='', preview='/Черешня.png')
        Blog.objects.create(title='клубника', body='', preview='/Клубника.png')






