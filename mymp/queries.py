import datetime
from main.models import *
from django.db import models

today = datetime.datetime.now()

t1 = StrategyTag.objects.create(name='стабильный доход')
t2 = StrategyTag.objects.create(name='низкая просадка')
StrategyTag.objects.all()

c1 = StrategyCategory.objects.create(name='Внутридневная')
c2 = StrategyCategory.objects.create(name='Среднесрочная')
c3 = StrategyCategory.objects.create(name='Позиционная')
StrategyCategory.objects.all()

a1 = StrategyAuthor(first_name='Иван', last_name='Иванов', email='author1@mail.ru')
a1.save()
a2 = StrategyAuthor(first_name='Петр', last_name='Петров', email='petrov@gmail.com')
a2.save()
StrategyAuthor.objects.all()

s1 = Strategy(title='Strategy 1',
              date_create=today,
              date_modify=today,
              category=c1,
              author=a1,
              annual_return=10)
s1.save()
s1.tags.add(t1, t2)
s2 = Strategy(title='Strategy 2',
              date_create=today,
              date_modify=today,
              category=c2,
              author=a1,
              annual_return=10)
s2.save()
s2.tags.add(t1)
s3 = Strategy(title='Strategy 3',
              date_create=today,
              date_modify=today,
              category=c2,
              author=a2,
              annual_return = -5)
s3.save()
s3.tags.add(t2)

Strategy.objects.all()
Strategy.objects.filter(id_category=1)
Strategy.objects.filter(id_category=2)