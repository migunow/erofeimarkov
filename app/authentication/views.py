#coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import View
from django.core.mail import send_mail, EmailMessage

from .models import User
from .forms import RegistrationForm


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('catalog:catalog'))
            else:
                ctx = {
                    'error_message': 'Ваш аккаунт заблокирован',
                }
                return render(request, 'authentication/login.html', ctx)
        else:
            ctx = {
                'error_message': 'Неверный email или пароль',
            }
            return render(request, 'authentication/login.html', ctx)


class LogOutView(View):
    def get(self, request):
        print('logout')
        logout(request)
        return HttpResponseRedirect(reverse('catalog:catalog'))

    def post(self, request):
        return self.get(request)


class RegistrationView(View):

    def get(self, request):
        return render(request, 'authentication/registration.html')

    @staticmethod
    def post(request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = User()
            new_user.username = form.cleaned_data['username']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.patronymic = form.cleaned_data['patronymic']
            new_user.phone = form.cleaned_data['phone']
            new_user.company_name = form.cleaned_data['company_name']
            new_user.city = form.cleaned_data['city']
            # new_user.call_from = form.cleaned_data['call_from']
            # new_user.call_to = form.cleaned_data['call_to']
            new_user.set_password(form.cleaned_data['password'])
            new_user.role = new_user.ROLE_CLIENT
            new_user.save()
            return HttpResponseRedirect(reverse('authentication:login'))
        else:
            ctx = {key: value for key, value in form.errors.items()}
            ctx['form'] = form
            return render(request, 'authentication/registration.html', ctx)


class RestorePasswordView(View):
    def get(self, request):
        return render(request, 'authentication/restore.html')

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            ctx = {
                'error_message': 'Вы не зарегистрированы',
            }
            return render(request, 'authentication/restore.html', ctx)

        new_password = user.generate_passwd()
        user.set_password(new_password)
        user.save()
        html_content = render_to_string('email_templates/restore_password.html', {
            "email": user.username,
            "password": new_password,
            "domain": 'ololo',
        })

        msg = EmailMessage()
        msg.subject = 'Восстановление пароля erofeimarkov.ru'
        msg.body = html_content
        msg.from_email = 'Erofeimarkov.ru <noreply@erofeimarkov.ru>'
        msg.to = [user.username]
        msg.content_subtype = "html"
        sent_count = msg.send()
        ctx = {
            'error_message': 'Вам отправлено письмо с новым паролем. Проверьте почту.',
        }
        return render(request, 'authentication/restore.html', ctx)


