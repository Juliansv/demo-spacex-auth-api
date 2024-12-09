from django.urls import re_path
from . import views

urlpatterns = [
    re_path('login', views.login),
    re_path('signup', views.signup),
    re_path('loggedIn', views.loggedIn),
    re_path('get_missions_data', views.get_missions_data),
]
