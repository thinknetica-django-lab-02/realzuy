from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField
from main.messages import *
from main.tasks import send_welcome_message_schedule

class Strategy(models.Model):
    title = models.CharField(max_length=64, verbose_name="Название")
    description = models.CharField(max_length=2056, verbose_name="Описание")
    date_create = models.DateField(verbose_name="Дата создания")
    date_modify = models.DateField(verbose_name="Дата последнего изменения")
    is_active = models.BooleanField(default=False, verbose_name='Состояние')
    id_category = models.ForeignKey('StrategyCategory', on_delete=models.CASCADE, verbose_name='Категория')
    id_author = models.ForeignKey('StrategyAuthor', on_delete=models.CASCADE, verbose_name="Автор")
    annual_return = models.FloatField(default=0, verbose_name="Годовая доходность")
    tags = models.ManyToManyField('StrategyTag')
    min_nav = models.IntegerField(null=False, verbose_name='Минимальный СЧА')
    pic_yield = ImageField(upload_to="pics/", verbose_name='График доходности', blank=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Стратегия'
        verbose_name_plural = 'Стратегии'

    @property
    def is_active_text(self):
        return "Активна" if self.is_active else "Не активна"

    @property
    def is_revenue(self):
        return True if self.annual_return > 0 else False

    def __str__(self):
        return self.title


class StrategyTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег для стратегий'
        verbose_name_plural = 'Теги для стратегий'

    def __str__(self):
        return self.name


class StrategyCategory(models.Model):
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class StrategyAuthor(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=254)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = 'Автор стратегии'
        verbose_name_plural = 'Авторы стратегий'

    def __str__(self):
        return self.full_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    avatar = ImageField(upload_to="users/", verbose_name='Аватар', blank=True)
    subscriptions = models.ManyToManyField('Subscription', verbose_name='Подписки', blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        grp, created = Group.objects.get_or_create(name='common users')
        instance.groups.add(grp)

        send_welcome_message_schedule.delay(instance.id)


class Subscription(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    class Meta:
        ordering = ['name']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return self.name
