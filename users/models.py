from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    phone = models.CharField(max_length=35, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар')
    country = models.CharField(max_length=100, verbose_name='Страна')
    token = models.CharField(max_length=100, verbose_name='Токен')
    is_moderator = models.BooleanField(default=False, verbose_name='Модератор')
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',  # добавленный related_name
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',  # добавленный related_name
        related_query_name='custom_user'
    )


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        # Проверка, если пользователь является модератором, добавляем его в группу "Модераторы"
        if self.is_moderator and not self.groups.filter(name='Модераторы').exists():
            group = Group.objects.get(name='Модераторы')
            self.groups.add(group)
        super().save(*args, **kwargs)


class BlogArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog')
    views = models.PositiveIntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
