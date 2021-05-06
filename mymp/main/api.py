from rest_framework import viewsets
from main.serializers import StrategySerializer
from main.models import Strategy
import django_filters


class StrategyFilter(django_filters.FilterSet):
    """Filter for strategies."""

    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Strategy
        fields = ['title', 'is_active']


class StrategyViewSet(viewsets.ModelViewSet):
    """Strategies API endpoint."""

    queryset = Strategy.objects.filter(is_archive=False)
    serializer_class = StrategySerializer
    filterset_class = StrategyFilter
    # filterset_fields = ['title', 'is_active']
