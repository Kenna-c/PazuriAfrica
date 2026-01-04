from django.contrib import admin

from .models import Module, Fee
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'module_code', 'duration_weeks', 'lecturer','student','lecturer', 'created_at')
    search_fields = ('title', 'module_code', 'lecturer__user__first_name', 'lecturer__user__last_name')
    list_filter = ('module_code', 'created_at')

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student','program', 'total_fees', 'paid_amount', 'balance')
    search_fields = ('student__user__first_name', 'student__user__last_name')
    list_filter = ('student','program')