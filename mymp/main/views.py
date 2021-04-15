from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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


def error_404(request, exception):
    return render(request, 'errors/404.html')


def index(request):
    return render(
        request,
        'index.html',
        context={'turn_on_block': True,
                 'some_text': 'Привет, мир!'},
    )


class StrategyList(ListView):
    model = Strategy
    context_object_name = 'strategies'
    queryset = Strategy.objects.order_by('-annual_return')
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(StrategyList, self).get_context_data(**kwargs)
        tag = self.request.GET.get('tag')
        context['tag'] = tag
        if tag is not None:
            context['tag_url'] = "&tag=" + tag
        else:
            context['tag_url'] = ""

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = self.request.GET.get('tag')
        if tag:
            return queryset.filter(tags__name=tag)
        return queryset


class StrategyDetail(DetailView):
    model = Strategy
    context_object_name = 'strategy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_author'] = self.request.user.groups.filter(name='Authors').exists()
        return context


class StrategyCreate(CreateView):
    model = Strategy
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Добавление стратегии"
        return context

    def get_success_url(self):
        return '/strategies/' + str(self.object.id) + '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and self.request.user.groups.filter(name='Authors').exists():
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)
        else:
            return redirect(settings.LOGIN_URL)


class StrategyUpdate(UserPassesTestMixin, UpdateView):
    model = Strategy
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Редактирование стратегии"
        return context

    def get_success_url(self):
        return '/strategies/' + str(self.object.id) + '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and self.request.user.groups.filter(name='Authors').exists():
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)
        else:
            return redirect(settings.LOGIN_URL)


@login_required
@transaction.atomic
def update_profile(request):
    User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])

    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        formset = ProfileFormset(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid() and formset.is_valid():
            u = user_form.save()
            for form in formset.forms:
                up = form.save(commit=False)
                up.user = u
                up.save()
            formset.save()  # иначе не сохраняется ManyToMany
            messages.success(request, 'Ваш профиль успешно обновлен!')
        else:
            messages.error(request, 'При обновлении профиля возникли ошибки')
    else:
        user_form = UserForm(instance=request.user)
        formset = ProfileFormset(instance=request.user)
    return render(request, 'profile.html', locals())


def phone_number_confirmation(request):
    user = request.user
    user_id = user.id
    phone_number = str(user.profile.phone_number)
    confirmation_flag = user.profile.is_phone_confirmed
    if not confirmation_flag and phone_number:
        send_sms_code.delay(phone_number, user_id)
        confirm_message = "Код подтверждения отправлен на Ваш номер телефона"
        request.session['confirm_message'] = confirm_message
        return redirect('profile')
    else:
        confirm_message = 'Вы уже подтвердили номер телефона ранее'
        request.session['confirm_message'] = confirm_message
        return redirect('profile')
