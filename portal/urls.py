from django.urls import path

from accounts import views
from .views import dashboard, fee_balace, staff_module_detail, student_dashboard, staff_dashboard, upload_results, view_assignments, view_lectures, logout
from .views import fee_payment, fee_history, staff_lectures
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('student/', student_dashboard, name='student_dashboard'),
    path('student/fee-balance/', fee_balace, name='fee_balance'),
    path('staff/', staff_dashboard, name='staff_dashboard'),
    #path('staff/', staff_dashboard, name='staff_dashboard'),
    path('staff/module/<int:module_id>/', staff_module_detail, name='staff_module_detail'),
    #path('staff/module/<int:module_id>/upload-results/', upload_results, name='upload_results'),
    path('student/lectures/', view_lectures, name='view_lectures'),
    path('student/assignments/', view_assignments, name='view_assignments'),
    path('logout/', logout, name='logout'),
    #path('student/fee-balance/', fee_balace, name='fee_balance'),
    path('student/fee-payment/', fee_payment, name='fee_payment'),
    path('student/fee-history/', fee_history, name='fee_history'),
    #path('staff/module-details/', staff_module_detail, name='staff_module_detail'),
    
    path(
        'staff/module/<int:module_id>/upload-results/', upload_results,
        name='upload_results'
        ),
    path('staff/lectures/', staff_lectures, name='staff_lectures'),

]
