from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('admin/', views.admin_panel, name='admin_panel'),
    path('add-entry/', views.add_entry, name='add_entry'),
    path('delete-entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('translate/', views.translate, name='translate'),
]