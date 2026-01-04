from django.contrib import admin

from .models import Program

@admin.register(Program)
class Program(admin.ModelAdmin):
    list_display = ('name', 'duration_months', 'level','study_mode', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    