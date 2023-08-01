from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from main.Blog.models import Blog
from main.latter.forms import SmsLetterForm, SubjectForm
from main.latter.models import SmsLetter, Mailing, Client


class SmsLetterCreateView(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    model = SmsLetter
    form_class = SmsLetterForm
    success_url = reverse_lazy("latter:create")

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save(commit=False)
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class SmsLetterListView(ListView):
    model = SmsLetter
    template_name = "latter/smsletter_list.html"
    permission_required = "latter.view_product"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


class SmsLetterUpdateView(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    model = SmsLetter
    fields = ("title", "client","send_time","frequency","status")
    permission_required = "main.Product.change_product"
    #success_url = reverse_lazy('Blog:list')

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     self.object.owner != self.request.user:
    #     raise Http404
    #     return self.object
    #
    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)   # СОХРАНЕНИЕ

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("Product:update", args=[self.kwargs.get('pk')])  # ПРИВЯЗКА ПО ПК

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(SmsLetter,Client, form=SubjectForm, extra=1)
        if self.request.method == "POST":  # пост и гет запрос
            context_data["formset"] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = SubjectFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()["formset"]
        self.object = form.save()
        if formset.is_valid():  # проверка на валидность возвращение и сохранение
            formset.instance = self.object
            formset.save()

            return super().form_valid(form)


class SmsLetterDetailView(DetailView):
    model = SmsLetter
    template_name = "latter/smsletter_detail.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()    # количество просмотров
        return self.object


class SmsLetterDeleteView(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    model = SmsLetter
    success_url = reverse_lazy("latter:list")
    permission_required = "latter.delete_product"

    def test_func(self):
        return self.request.user.is_superuser


def index(request):
    # Получаем количество рассылок всего
    total_newsletters = SmsLetter.objects.count()

    # Получаем количество активных рассылок
    active_newsletters = SmsLetter.objects.filter(is_active=True).count()

    # Получаем количество уникальных клиентов для рассылок
    unique_clients = Client.objects.filter(client__isnull=False).distinct().count()

    # Получаем 3 случайные статьи из блога
    blog_posts = Blog.objects.order_by('?')[:3]

    context = {
        'total_newsletters': total_newsletters,
        'active_newsletters': active_newsletters,
        "unique_clients": unique_clients,
        'blog_posts': blog_posts,
    }

    return render(request, 'latter/information.html', context)

def smslatters(request):
    SmsLetter_list = SmsLetter.objects.all()
    context = {
        'sms_lat': SmsLetter_list,
        "title": "Главная",
    }
    return render(request, "latter/smsletter_list.html", context)


def catalog(request, pk):
    context = {
        'all': SmsLetter.objects.filter(id=pk),
        "title": "Главная",
    }
    return render(request, "latter/smsletter_detail.html", context)


def send_email(request):
    mailing = Mailing.objects.get(title="Важно")  # Get the specific Mailing object with the desired title
    title = mailing.title
    content = mailing.content
    clients = Client.objects.all()
    recipient_list = [client.email for client in clients]
    send_mail(title, content, settings.EMAIL_HOST_USER, recipient_list)
    return render(request, "latter/email_complete.html")

