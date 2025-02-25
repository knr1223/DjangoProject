from django.urls import path
from . import views

urlpatterns = [
    path('', views.print_hello, name='hello'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('users/', views.all_users, name='all_users'),
    path('user/<str:email>/', views.get_user_by_email, name='single_user'),
]
