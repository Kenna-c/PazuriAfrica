from django.urls import path
from . import views
#from views import apply

urlpatterns = [
    path('', views.apply, name='apply'),
]