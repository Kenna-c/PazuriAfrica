from django.contrib import admin
from django.utils.crypto import get_random_string
from admissions.models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'program', 'submitted_at', 'status', 'admission_number')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'program__name')
    list_filter = ('program', 'submitted_at')
    readonly_fields = ('submitted_at',)

    def save_model(self, request, obj, form, change):
        if not obj.admission_number and obj.status == 'Accepted':
            obj.admission_number = f"PAC-{get_random_string(6).upper()}"
        super().save_model(request, obj, form, change)

# Register other models if needed