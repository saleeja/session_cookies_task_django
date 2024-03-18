from django.urls import path
# from django.contrib.auth.views import LoginView
from .views import *

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('items/', list_items, name='list_items'),
    path('login-attempts/', login_attempts, name='login_attempts'),
]


