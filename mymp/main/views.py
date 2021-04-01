from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Strategy

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
