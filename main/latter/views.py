from django.conf import settings
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from main.latter.forms import SmsLetterForm, SubjectForm
from main.latter.models import SmsLetter, Mailing, Client


class SmsLetterCreateView(CreateView):
    model = SmsLetter
    form_class = SmsLetterForm
    success_url = reverse_lazy("latter:create")
    permission_required = "main.latter.add_latter"

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save(commit=False) # создаем объект, но не сохраняем его в базе данных
            new_mat.slug = slugify(new_mat.title) # устанавливаем значение атрибута "slug"
            new_mat.save() # сохраняем объект в базе данных

        return super().form_valid(form)


class SmsLetterListView(ListView):
    model = SmsLetter
    template_name = "latter/smsletter_list.html"
    permission_required = "latter.view_product"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


class SmsLetterUpdateView(UpdateView):
    model = SmsLetter
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
        SubjectFormset = inlineformset_factory(SmsLetter, Subject, form=SubjectForm, extra=1)
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


class SmsLetterDeleteView(DeleteView):
    model = SmsLetter
    success_url = reverse_lazy("latter:list")

    def test_func(self):
        return self.request.user.is_superuser


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

    # Get the list of clients
    clients = Client.objects.all()

    # Create a list of email addresses from the clients list
    recipient_list = [client.email for client in clients]

    # Send the email to all addresses in recipient_list
    send_mail(title, content, settings.EMAIL_HOST_USER, recipient_list)
    return render(request, "latter/email_complete.html")


