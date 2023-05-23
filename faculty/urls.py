from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_teacher, name='login'),
    path('logout/', logout_teacher, name='logout'),
    path('register/', register_teacher, name='register'),
    path('create_school', create_school, name='create_school'),
    path('join_school', join_school, name='join_school'),
    path('faculties_configure', faculties_configure, name='faculties_configure'),
    path('profile/main_data/', profile_main_data, name='profile_main_data'),
]