from . import views
from .views import *
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('strategies/', StrategyList.as_view(), name='strategies'),
    path('strategies/<int:pk>/', StrategyDetail.as_view(), name='strategy-detail'),
    path('accounts/profile/', views.update_profile, name='profile-update'),
    path('accounts/profile/phone_confirm', views.phone_number_confirmation, name='phone-confirm'),
    path('strategies/add/', StrategyCreate.as_view(), name='strategy-form'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('strategies/<int:pk>/edit/', StrategyUpdate.as_view(), name='strategy-form'),
]
handler404 = error_404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)