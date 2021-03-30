
from django.db import models


class Strategy(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=2056)
    date_create = models.DateField()
    date_modify = models.DateField()
    is_active = models.BooleanField(default=False)
    id_category = models.ForeignKey('StrategyCategory', on_delete=models.CASCADE)
    id_author = models.ForeignKey('StrategyAuthor', on_delete=models.CASCADE)
    annual_return = models.FloatField(default=0)
    tags = models.ManyToManyField('StrategyTag')
    min_nav = models.IntegerField(null=False, verbose_name='Минимальный СЧА')

    class Meta:
        ordering = ['title']
        verbose_name = 'Стратегия'
        verbose_name_plural = 'Стратегии'

    @property
    def is_revenue(self):
        return True if self.annual_return > 0 else False

    def __str__(self):
        return self.title


class StrategyTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

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
