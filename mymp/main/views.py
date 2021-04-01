from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib import messages

from .forms import UserForm
from .models import Strategy, Profile



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
    paginate_by = 10

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

@login_required
@transaction.atomic
def update_profile(request):
    User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
    ProfileFormset = inlineformset_factory(User, Profile, fields='__all__', can_delete=False)
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
