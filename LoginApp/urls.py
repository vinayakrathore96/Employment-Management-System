from django.urls import path

from . import views

from django.contrib.auth import views as auth_views



urlpatterns = [

    path('',views.login,name='login'),

    path('register/',views.register,name='register'),

    path('home/',views.home,name='home'),

    path('home/logout/',views.logout,name='logout'),

    path('home/change_password/',views.change_password,name='change_password'),

    path('home/profile/edit_profile/',views.edit_profile,name='edit_profile'),

    path('home/profile/',views.profile,name='profile'),

    path('home/employees_list',views.employees_list,name='employees_list'),

    path('home/deactivate_user',views.deactivate_user,name='deactivate_user'),

path('reset_password/',

     auth_views.PasswordResetView.as_view(template_name="password_reset.html"),

     name="reset_password"),



    path('reset_password_sent/',

        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),

        name="password_reset_done"),



    path('reset/<uidb64>/<token>/',

     auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),

     name="password_reset_confirm"),



    path('reset_password_complete/',

        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),

        name="password_reset_complete"),





]
