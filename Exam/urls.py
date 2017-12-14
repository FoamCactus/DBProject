from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
urlpatterns = [
    url(r'^$', views.index , name='index'),
    url(r'^login/', views.login , name='login'),
    url(r'^studentSignIn/', views.studentSignIn, name='studentSignIn'),
    url(r'^TeacherLogin/$', auth_views.login, name='login'),
    url(r'^TeacherLogout/$',auth_views.logout, {'next_page': '/'}, name='logout'),
]