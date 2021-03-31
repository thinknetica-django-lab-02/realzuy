from django.shortcuts import render

def index(request):
    return render(
        request,
        'index.html',
        context={'turn_on_block': True},
    )