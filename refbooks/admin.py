import datetime

from django.contrib import admin
from django import forms

from .models import Refbook, Version, Element


class VersionInline(admin.TabularInline):
    model = Version
    readonly_fields = ('version', 'date',)
    verbose_name_plural = 'Версии справочника'

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Refbook)
class RefbookAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'get_last_version', 'get_date_version']
    list_display_links = ['code', 'name']
    list_per_page = 10
    inlines = [VersionInline]

    def get_last_version(self, obj):
        date_today = datetime.datetime.now()
        return obj.versions.values_list('version').filter(date__lte=date_today). \
            order_by('date').last()
    get_last_version.short_description = "Текущая версия"

    def get_date_version(self, obj):
        date_today = datetime.datetime.now()
        return obj.versions.values_list('date').filter(date__lte=date_today). \
            order_by('date').last()
    get_date_version.short_description = "Дата начала действия версии"


class ElementsInline(admin.TabularInline):
    model = Element
    extra = 0


class RefbookChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{} - код {}".format(obj.name, obj.code)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ['get_code_refbook', 'get_refbook', 'version', 'date']
    list_display_links = ['version', 'date']
    list_filter = ['refbook', 'date']
    list_per_page = 10
    inlines = [ElementsInline]

    def get_code_refbook(self, obj):
        return obj.refbook.code
    get_code_refbook.short_description = 'Код справочника'

    def get_refbook(self, obj):
        return obj.refbook.name
    get_refbook.short_description = 'Наименование справочника'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'refbook':
            return RefbookChoiceField(queryset=Refbook.objects.all(), label='Справочник')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class VersionChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}, версия {}".format(obj.refbook, obj.version)


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ['id', 'version', 'code', 'value']
    list_display_links = ['code', 'value']
    list_filter = ['version']
    list_per_page = 10

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'version':
            return VersionChoiceField(queryset=Version.objects.order_by('refbook', 'version'), label='Версия')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
