from . import views
from .views import StrategyList, StrategyDetail, StrategyCreate, StrategyUpdate, error_404
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('strategies/', StrategyList.as_view(), name='strategies'),
    path('strategies/<int:pk>/', StrategyDetail.as_view(), name='strategy-detail'),
    path('accounts/profile/', views.update_profile, name='profile-update'),
    path('strategies/add/', StrategyCreate.as_view(), name='strategy-form'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('strategies/<int:pk>/edit/', StrategyUpdate.as_view(), name='strategy-form'),
]
handler404 = error_404
