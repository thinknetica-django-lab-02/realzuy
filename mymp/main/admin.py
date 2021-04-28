from django.contrib import admin
from django.db import models
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from ckeditor.widgets import CKEditorWidget
from django.db.models import QuerySet
from django.http import HttpRequest

from main.models import Strategy, \
    StrategyCategory, StrategyTag, Profile, \
    Subscription, SMSLog


class FlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)


@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):

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
    readonly_fields = ('date_create',)

    fieldsets = (
        ('General Info', {
            'fields': ('title', 'is_active', 'is_archive', 'id_category', 'min_nav')
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('id_author', 'tags'),
        })
    )


@admin.register(StrategyCategory)
class StrategyCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(StrategyTag)
class StrategyTagAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    pass
