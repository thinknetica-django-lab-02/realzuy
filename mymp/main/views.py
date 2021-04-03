from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import auth
from .forms import UserForm, ProfileFormset
from .models import Strategy, Profile


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
        if request.user.is_authenticated:
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)
        else:
            return redirect("login")


class StrategyUpdate(UpdateView):
    model = Strategy
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Редактирование стратегии"
        return context

    def get_success_url(self):
        return '/strategies/' + str(self.object.id) + '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)
        else:
            return redirect("login")


@login_required
@transaction.atomic
def update_profile(request):
    User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        formset = ProfileFormset(request.POST, instance=request.user.profile)
        if user_form.is_valid() and formset.is_valid():
            u = user_form.save()
            for form in formset.forms:
                up = form.save(commit=False)
                up.user = u
                up.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
        else:
            messages.error(request, 'При обновлении профиля возникли ошибки')
    else:
        user_form = UserForm(instance=request.user)
        formset = ProfileFormset(instance=request.user.profile)
    return render(request, 'profile.html', locals())
