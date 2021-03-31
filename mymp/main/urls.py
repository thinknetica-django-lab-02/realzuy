from django.urls import path
from . import views
from .views import StrategyList, StrategyDetail

urlpatterns = [
    path('', views.index, name='index'),
    path('strategies/', StrategyList.as_view(), name='strategies'),
    path('strategies/<int:pk>/', StrategyDetail.as_view(), name='strategy-detail'),
]