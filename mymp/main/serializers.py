from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from main.models import Strategy, StrategyAuthor, StrategyCategory


class StrategySerializer(serializers.ModelSerializer):
    """Strategy serializer."""

    id_author = SlugRelatedField(queryset=StrategyAuthor.objects.all(), slug_field='email')
    id_category = SlugRelatedField(queryset=StrategyCategory.objects.all(), slug_field='name')

    class Meta:
        model = Strategy
        fields = ('title', 'description',  'annual_return',
                  'is_active', 'min_nav', 'tags', 'pic_yield',
                  'id_category', 'id_author')
