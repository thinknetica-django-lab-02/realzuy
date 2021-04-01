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

class StrategyDetail(DetailView):
    model = Strategy
    context_object_name = 'strategy'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        #context['book_list'] = Book.objects.all()
        return context