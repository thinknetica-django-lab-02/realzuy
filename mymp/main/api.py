from rest_framework import viewsets
from main.serializers import StrategySerializer
from main.models import Strategy


class StrategyViewSet(viewsets.ModelViewSet):
    """Strategies API endpoint."""

    queryset = Strategy.objects.filter(is_archive=False)
    serializer_class = StrategySerializer
