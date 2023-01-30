from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'

    ROLE_CHOICES = [(USER, 'Пользователь'),
                    (ADMIN, 'Администратор')]

    username = models.CharField(
        verbose_name='Логин пользователя',
        max_length=150,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
    )
    role = models.CharField(
        verbose_name='Статус',
        choices=ROLE_CHOICES,
        default=USER,
        max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    
    @property
    def is_admin(self):
        return self.is_superuser or self.is_staff or self.role == User.ADMIN

    @property
    def is_block(self):
        return self.role == User.BLOCK
    
    def __str__(self):
        return self.username

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
