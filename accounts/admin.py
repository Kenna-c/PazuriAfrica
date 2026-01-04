from django.contrib import admin
from .models import Profile, Instructor, Student, AccountSettings, PaymentMethod, Transaction, Staff
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'birth_date')
    list_filter = ('location', 'birth_date')
    search_fields = ('user__username', 'location')

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('profile', 'hire_date', 'department')
    list_filter = ('department',)
    search_fields = ('profile__user__username',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'enrollment_date', 'admission_number', 'is_active')
    list_filter = ('admission_number',)
    search_fields = ('profile__user__username',)

@admin.register(AccountSettings)
class AccountSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notifications', 'sms_notifications')
    list_filter = ('email_notifications', 'sms_notifications')
    search_fields = ('user__username',)

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'method_type')
    search_fields = ('user__username',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_date')
    list_filter = ('status',)
    search_fields = ('reference_code','user__username')

    def __str__(self):
        return f"Transaction {self.reference_code} - {self.status}"
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('profile', 'staff_id', 'position', 'department', 'hire_date')
    list_filter = ('department',)
    search_fields = ('profile__user__username',)