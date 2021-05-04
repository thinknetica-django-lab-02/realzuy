from django.contrib import admin
from django.db import models
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from ckeditor.widgets import CKEditorWidget
from django.db.models import QuerySet
from django.http import HttpRequest

from main.models import Strategy, \
    StrategyCategory, Profile, \
    Subscription, SMSLog, StrategyAuthor


class FlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)


@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    """Стратегия"""
    def make_archived(self, request: HttpRequest, queryset: QuerySet) -> None:
        queryset.update(is_archive=True)

    make_archived.short_description = "Добавить в архив"

    def make_unarchived(self, request: HttpRequest, queryset: QuerySet) -> None:
        queryset.update(is_archive=False)

    make_unarchived.short_description = "Убрать из архива"

    def make_active(self, request: HttpRequest, queryset: QuerySet) -> None:
        queryset.update(is_active=True)

    make_active.short_description = "Сделать активными"

    def make_inactive(self, request: HttpRequest, queryset: QuerySet) -> None:
        queryset.update(is_active=False)

    make_inactive.short_description = "Сделать неактивными"

    actions = [make_archived, make_unarchived, make_active, make_inactive]
    list_filter = ('id_category', 'is_active', 'is_archive', 'id_author', 'tags')
    search_fields = ('title', 'description')
    readonly_fields = ('description',)

    list_display = (
        'id', 'title', 'description', 'id_category', 'id_author', 'date_create', 'date_modify', 'is_active', 'is_archive', 'min_nav','tags')

    fieldsets = (
        ('General Info', {
            'fields': ('title', 'description', 'is_active', 'is_archive', 'id_category', 'min_nav')
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('id_author', 'tags', 'date_create', 'date_modify'),
        })
    )


@admin.register(StrategyCategory)
class StrategyCategoryAdmin(admin.ModelAdmin):
    """Категории стратегий"""


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Профили пользователей"""


@admin.register(StrategyAuthor)
class StrategyAuthorAdmin(admin.ModelAdmin):
    """Автор"""
    list_display = (
        'id', 'first_name', 'last_name', 'email')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Подписки"""


@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    """Журнал смс"""
