from django.urls import path
from .views import pay_fees, mpesa_callback

urlpatterns = [
    path('pay/', pay_fees, name='pay_fees'),
    path('callback/', mpesa_callback),
]
