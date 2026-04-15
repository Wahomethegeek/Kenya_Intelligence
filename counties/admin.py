from django.contrib import admin
from .models import County

@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'region', 'population']
    search_fields = ['name', 'region']
    ordering = ['code']
