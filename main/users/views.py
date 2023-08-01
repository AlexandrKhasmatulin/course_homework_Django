# Create your views here.
import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.shortcuts import render, redirect
from main.users.forms import UserRegisterForm, UserProfileForm, EmailVerificationForm
from main.users.models import User, UserVerification


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        print(form.cleaned_data)
        response = super().form_valid(form)
        user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])  # регистрация
        if user is not None:
            login(self.request, user)
        return response


class PasswordResetCustomView(PasswordResetView):
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('users:password_reset_done')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

def verify(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        user_verification = UserVerification.objects.get(verification_code=verification_code)
        user_verification.is_verified = True
        user_verification.save()
        return redirect('/')
    else:
        return render(request, 'verification/verify.html')


def send_verification_email(request):
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            verification_code = str(random.randint(100000, 999999))
            UserVerification.objects.create(user=user, verification_code=verification_code)
            send_mail(
                'Verification code',
                f'Ваш код для авторизации {verification_code}',
                'margoonavt@yandex.ru',
                [email],
                fail_silently=False,
            )
            return redirect('users:verify')
    else:
        form = EmailVerificationForm()
    return render(request, 'verification/send_verification_email.html', {'form': form})


