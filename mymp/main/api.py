from rest_framework import viewsets
from main.serializers import StrategySerializer
from main.models import Strategy
import django_filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission


class StrategyFilter(django_filters.FilterSet):
    """Filter for strategies."""

    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Strategy
        fields = ['title', 'is_active']


class HasStrategyPermissions(BasePermission):
    """Check user permissions to modify strategies."""
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.groups.filter(name='Authors').exists())


class StrategyViewSet(viewsets.ModelViewSet):
    """Strategies API endpoint."""

    queryset = Strategy.objects.filter(is_archive=False)
    serializer_class = StrategySerializer
    filterset_class = StrategyFilter

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = [HasStrategyPermissions]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
