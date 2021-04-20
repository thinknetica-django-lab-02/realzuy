from django.contrib.auth.models import User
from django.test import TestCase
from .models import Strategy, StrategyTag, StrategyCategory, StrategyAuthor
from django.urls import reverse
import datetime

today = datetime.datetime.now()


class MainViewsTest(TestCase):
    """Тесты представлений"""
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(
            email='user1@mail.com',
            username='user1@mail.com',
            first_name='User1 fn',
            last_name='User1 ln',
            password='user1',
        )
        user1.save()

        number_of_tags = 2
        for num in range(number_of_tags):
            StrategyTag.objects.create(
                name='tag %s' % num, )

        number_of_categories = 5
        for num in range(number_of_categories):
            StrategyCategory.objects.create(
                name='category %s' % num, )

        number_of_authors = 5
        for num in range(number_of_authors):
            StrategyAuthor.objects.create(
                first_name='fname %s' % num,
                last_name='lname %s' % num, )

        number_of_strategies = 33
        for num in range(number_of_strategies):
            Strategy.objects.create(
                title='Strategy %s' % num,
                date_create=today,
                date_modify=today,
                id_category=StrategyCategory.objects.get(id=1),
                id_author=StrategyAuthor.objects.get(id=1),
                min_nav=100,
                annual_return=10)

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_strategies_list_url_accessible(self):
        """Проверка доступности списка стратегий"""
        response = self.client.get(reverse('strategies'))
        self.assertEqual(response.status_code, 200)

    def test_strategy_view_url_accessible(self):
        """Проверка доступности карточки стратегии"""
        strategy = Strategy.objects.create(
            title='Strategy xi',
            date_create=today,
            date_modify=today,
            id_category=StrategyCategory.objects.get(id=1),
            id_author=StrategyAuthor.objects.get(id=1),
            min_nav=100,
            annual_return=10)
        response = self.client.get('/strategies/%d/' % (strategy.id,))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_url_not_accessible(self):
        """Проверка переадресации на страницу логина
        при попытке обращения неавторизованного пользователя
        к странице профиля"""
        response = self.client.get(reverse('profile-update'))
        self.assertRedirects(response, '/accounts/login/')

    def test_profile_view_url_accessible(self):
        """Проверка доступности страницы профиля
        для авторизованного пользователя"""
        self.client.login(username='user1@mail.com',
                          password='user1')
        response = self.client.get(reverse('profile-update'))
        self.assertEqual(response.status_code, 200)

    def test_strategies_pagination_is_five(self):
        """Проверка пагинации списка стратегий"""
        resp = self.client.get(reverse('strategies'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['strategies']) == 5)

    def test_strategies_list_view_uses_correct_template(self):
        """Проверка использования списком стратегий правильного шаблона"""
        resp = self.client.get(reverse('strategies'))
        self.assertTemplateUsed(resp, 'main/strategy_list.html')

    def test_strategy_view_uses_correct_template(self):
        """Проверка использования карточкой стратегии правильного шаблона"""
        strategy = Strategy.objects.create(
            title='Strategy xi',
            date_create=today,
            date_modify=today,
            id_category=StrategyCategory.objects.get(id=1),
            id_author=StrategyAuthor.objects.get(id=1),
            min_nav=100,
            annual_return=10)
        response = self.client.get('/strategies/%d/' % (strategy.id,))
        self.assertTemplateUsed(response, 'main/strategy_detail.html')
