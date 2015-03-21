#coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import random
import string

from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, username, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        username = self.normalize_email(username)
        user = self.model(username=username,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, False, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    username = models.EmailField('username', unique=True, blank=False)
    first_name = models.CharField('first name', max_length=300, blank=False)
    last_name = models.CharField('last name', max_length=50, blank=True)
    patronymic = models.CharField('patronymic', max_length=50, blank=True)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    phone = models.CharField('phone', max_length=20, blank=False)
    company_name = models.CharField('Название компании(для оптовиков)', max_length=100)
    city = models.CharField('Город(для оптовиков)', max_length=100)
    call_from = models.TimeField(verbose_name='Звонить с', blank=True, null=True)
    call_to = models.TimeField(verbose_name='Звонить по', blank=True, null=True)

    #Бесправная субстанция
    ROLE_NOBODY = 1
    #Обычный покупатель
    ROLE_CLIENT = 2
    #Оптовик
    ROLE_WHOLESALER = 3
    #Модератор/Администратор
    ROLE_STAFF = 4
    #Разработчик
    ROLE_DEVELOPER = 5
    ROLE_CHOICES = (
        (ROLE_NOBODY, 'Забанен/закрыт'),
        (ROLE_CLIENT, 'Покупатель'),
        (ROLE_WHOLESALER, 'Оптовик'),
        (ROLE_STAFF, 'Модератор'),
        (ROLE_DEVELOPER, 'Разработчик'),
    )

    role = models.PositiveSmallIntegerField('User role', choices=ROLE_CHOICES, default=ROLE_NOBODY)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('first_name', 'last_name', )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '{0} {1} {2}'.format(self.last_name, self.first_name, self.patronymic)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.username])

    def generate_passwd(self):
        a = string.ascii_letters + string.digits
        return ''.join([random.choice(a) for i in range(7)])
