from django.contrib import admin

from .models import Building, Unit


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name','address']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['num_bedrooms']
