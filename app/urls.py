from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'app'


urlpatterns = [
    #маршрутизация логина
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # форма
    path('form/<int:id>', views.form, name='form'),
    path('form/success', views.form_submit, name='form_submit'),

    # организация
    path('', views.index, name='index'),
    path('group/<int:id>', views.group_detail, name='group_detail'),
    path('finish/<int:id>', views.finish, name='finish'),

    # CRUD
    path('<object>/new', views.new, name='new'),
    path('<object>/<int:id>/edit', views.edit, name='edit'),
    path('<object>/<int:group_id>/<int:id>/delete', views.delete, name='delete'),
]