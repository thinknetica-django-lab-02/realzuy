from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField
from .tasks import send_welcome_message_schedule
from phonenumber_field.modelfields import PhoneNumberField


class Strategy(models.Model):
    """Стратегия"""
    title = models.CharField(max_length=64,
                             verbose_name="Название")
    """Название стратегии"""
    description = models.CharField(max_length=2056,
                                   verbose_name="Описание")
    """Краткое описание стратегии"""
    date_create = models.DateField(verbose_name="Дата создания")
    """Дата создания стратегии"""
    date_modify = models.DateField(verbose_name="Дата последнего изменения")
    """Дата последнего изменения стратегии"""
    is_active = models.BooleanField(default=False,
                                    verbose_name='Состояние')
    """Активна ли стратегия на текущий момент True=Активна"""
    id_category = models.ForeignKey('StrategyCategory',
                                    on_delete=models.CASCADE,
                                    verbose_name='Категория')
    """Категория стратегии"""
    id_author = models.ForeignKey('StrategyAuthor',
                                  on_delete=models.CASCADE,
                                  verbose_name="Автор")
    """Автор стратегии"""
    annual_return = models.FloatField(default=0,
                                      verbose_name="Годовая доходность")
    """Годовая доходность"""
    tags = models.ManyToManyField('StrategyTag')
    """Теги"""
    min_nav = models.IntegerField(null=False,
                                  verbose_name='Минимальный СЧА')
    """Минимальный СЧА для работы стратегии"""
    pic_yield = ImageField(upload_to="pics/",
                           verbose_name='График доходности',
                           blank=True)
    """Картинка с графиком изменения СЧА"""

    class Meta:
        ordering = ['title']
        verbose_name = 'Стратегия'
        verbose_name_plural = 'Стратегии'

    @property
    def is_active_text(self) -> str:
        return "Активна" if self.is_active else "Не активна"

    @property
    def is_revenue(self) -> bool:
        return True if self.annual_return > 0 else False

    def __str__(self) -> str:
        return self.title


class StrategyTag(models.Model):
    """Теги для стратегий"""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег для стратегий'
        verbose_name_plural = 'Теги для стратегий'

    def __str__(self) -> str:
        return self.name


class StrategyCategory(models.Model):
    """Категории для стратегий"""
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class StrategyAuthor(models.Model):
    """Автор стратегии"""
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=254)

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = 'Автор стратегии'
        verbose_name_plural = 'Авторы стратегий'

    def __str__(self) -> str:
        return self.full_name


class Profile(models.Model):
    """Профиль пользователя"""
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    birth_date = models.DateField(null=True,
                                  blank=True,
                                  verbose_name='Дата рождения')
    avatar = ImageField(upload_to="users/",
                        verbose_name='Аватар',
                        blank=True)
    subscriptions = models.ManyToManyField('Subscription',
                                           verbose_name='Подписки',
                                           blank=True)
    phone_number = PhoneNumberField(verbose_name='Номер телефона',
                                    blank=True)
    is_phone_confirmed = models.BooleanField(
        default=False, verbose_name='Телефон подтвержден')

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
    """Подписка"""
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name='Название')

    class Meta:
        ordering = ['name']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return self.name


class SMSLog(models.Model):
    """Журнал отправки смс"""
    code = models.PositiveIntegerField()
    receiver = models.CharField(max_length=32)
    status = models.CharField(max_length=32)
    date_create = models.DateTimeField(auto_now_add=True)
    date_sent = models.DateTimeField(auto_now_add=True)
