from django.core.management.base import BaseCommand, CommandError
from factory import SubFactory
from factory.django import DjangoModelFactory
from main.models import Strategy, StrategyCategory, StrategyAuthor
from datetime import datetime
from faker import Factory

faker = Factory.create()
today = datetime.now()


class StrategyCategoryFactory(DjangoModelFactory):
    class Meta:
        model = StrategyCategory
        django_get_or_create = ('name',)

    name = faker.word()


class StrategyAuthorFactory(DjangoModelFactory):
    class Meta:
        model = StrategyAuthor
        django_get_or_create = ('email',)

    first_name = faker.name()
    last_name = faker.name()
    email = faker.email()


class StrategyFactory(DjangoModelFactory):
    class Meta:
        model = Strategy

    title = faker.word()
    date_create = today
    date_modify = today
    id_category = SubFactory(StrategyCategoryFactory, name='Внутридневная')
    id_author = SubFactory(StrategyAuthorFactory, email='a@a.ru')
    min_nav = faker.random_int()
    annual_return = faker.random_int()


class Command(BaseCommand):
    help = 'Генерация тестовых данных для модели'

    def handle(self, *args, **options):
        try:
            strategy = StrategyFactory.create()
            self.stdout.write(self.style.SUCCESS('strategy created: ' + strategy.title))
        except Exception as e:
            raise CommandError('error: ' + str(e))
