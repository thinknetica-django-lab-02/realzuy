from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from .forms import UserForm, ProfileFormset
from .models import Strategy, Profile
from django.conf import settings
from .tasks import send_sms_code
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from typing import Dict, Any, Union

def error_404(request: HttpRequest, exception) -> HttpResponse:
    return render(request, 'errors/404.html')


def index(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'index.html',
        context={'turn_on_block': True,
                 'some_text': 'Привет, мир!'},
    )


class StrategyList(ListView):
    """Представление со списком стратегий"""
    model = Strategy
    context_object_name = 'strategies'
    queryset = Strategy.objects.order_by('-annual_return')
    paginate_by = 5

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super(StrategyList, self).get_context_data(**kwargs)
        tag = self.request.GET.get('tag')
        context['tag'] = tag
        if tag is not None:
            context['tag_url'] = "&tag=" + tag
        else:
            context['tag_url'] = ""

        return context

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        tag = self.request.GET.get('tag')
        if tag:
            return queryset.filter(tags__name=tag)
        return queryset


class StrategyDetail(DetailView):
    """Представление с карточкой стратегии"""
    template_name = 'main/strategy_detail.html'
    model = Strategy
    context_object_name = 'strategy'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_is_author'] = \
            self.request.user.groups.filter(name='Authors').exists()

        counter_name = f'view_counter_{context["strategy"].id}'
        view_counter = cache.get(counter_name, 0)
        view_counter += 1
        cache.set(counter_name, view_counter, timeout=60)
        context['view_counter'] = view_counter

        return context


class StrategyCreate(CreateView):
    """Форма создания стратегии"""
    model = Strategy
    fields = '__all__'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Добавление стратегии"
        return context

    def get_success_url(self) -> str:
        return '/strategies/' + str(self.object.id) + '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and \
                self.request.user.groups.filter(name='Authors').exists():
            if request.method.lower() in self.http_method_names:
                handler = getattr(self,
                                  request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)
        else:
            return redirect(settings.LOGIN_URL)


class StrategyUpdate(UserPassesTestMixin, UpdateView):
    """Форма редактирования стратегии"""
    model = Strategy
    fields = '__all__'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Редактирование стратегии"
        return context

    def get_success_url(self) -> str:
        return '/strategies/' + str(self.object.id) + '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and \
                self.request.user.groups.filter(name='Authors').exists():
            if request.method.lower() in self.http_method_names:
                handler = getattr(self,
                                  request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)
        else:
            return redirect(settings.LOGIN_URL)


@login_required
@transaction.atomic
def update_profile(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)

    User.profile = property(
        lambda u: Profile.objects.get_or_create(user=u)[0])

    if request.method == 'POST':
        user_form = UserForm(request.POST,
                             request.FILES,
                             instance=request.user)
        formset = ProfileFormset(request.POST,
                                 request.FILES,
                                 instance=request.user)
        if user_form.is_valid() and formset.is_valid():
            u = user_form.save()
            for form in formset.forms:
                up = form.save(commit=False)
                up.user = u
                up.save()
            formset.save()  # иначе не сохраняется ManyToMany
            messages.success(request,
                             'Ваш профиль успешно обновлен!')
        else:
            messages.error(request,
                           'При обновлении профиля возникли ошибки')
    else:
        user_form = UserForm(instance=request.user)
        formset = ProfileFormset(instance=request.user)
    return render(request, 'profile.html', locals())


def phone_number_confirmation(request: HttpRequest) -> HttpResponse:
    user = request.user
    user_id = user.id
    phone_number = str(user.profile.phone_number)
    confirmation_flag = user.profile.is_phone_confirmed
    if not confirmation_flag and phone_number:
        send_sms_code.delay(phone_number, user_id)
        confirm_message = "Код подтверждения отправлен на Ваш номер телефона"
        request.session['confirm_message'] = confirm_message
        return redirect('profile-update')
    else:
        confirm_message = 'Вы уже подтвердили номер телефона ранее'
        request.session['confirm_message'] = confirm_message
        return redirect('profile-update')
