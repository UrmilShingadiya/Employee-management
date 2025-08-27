from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'), 
    path('generate-offer-letter/', views.generate_offer_letter, name='generate_offer_letter'),
    path('generate-joining-letter/', views.generate_joining_letter, name='generate_joining_letter'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('employees/', views.all_employees, name='all_employees'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employee/<int:pk>/toggle-status/', views.toggle_employee_status, name='toggle_employee_status'),
    path('dashboard/', views.dashboard, name='dashboard'),


]

