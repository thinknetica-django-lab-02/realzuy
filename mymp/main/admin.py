from django.contrib import admin
from django.db import models
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from ckeditor.widgets import CKEditorWidget
from main.models import *


class FlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    pass

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
class ProfileAdmin(admin.ModelAdmin):
    pass