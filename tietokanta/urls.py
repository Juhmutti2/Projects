from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_page, name='test_page'),  # Testisivu osoitteessa /
    path('triathlon_records/', views.record_list, name='triathlon_record_list'),  
]
