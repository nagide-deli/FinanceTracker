from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('landingpage/', views.landingpage, name='landingpage'),
    path('contact_us/', views.contact_us, name='contact_us'),
]
