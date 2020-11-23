from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_company, name="register"),
    path('company/update/', views.update_company, name="update_company"),
    path('register_user/', views.register_user, name="register_user"),

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('home/', views.home, name="home"),

    path('users/', views.users, name="users"),
    path('users/create/', views.user_create, name="user_create"),
    path('users/update/<str:pk>/', views.user_update, name="user_update"),


    path('members/', views.members, name="members"),
    path('members_inactive/', views.members_inactive, name="members_inactive"),    
    path('members/detail/<str:pk>/', views.member_detail, name="member_detail"),  
    path('members/details/<str:pk>/', views.member_details, name="member_details"),
    path('members/payment/<str:pk>/', views.member_income_create, name="member_income_create"),
    path('members/payment/<str:mb>/<str:ik>', views.member_income_update, name="member_income_update"),
    
    path('members/create/', views.member_create, name="member_create"),
    path('members/update/<str:pk>/', views.member_update, name="member_update"),
    path('members/delete/<str:pk>/', views.member_delete, name="member_delete"),

    path('trainers/', views.trainers, name="trainers"),
    path('trainers/create/', views.trainer_create, name="trainer_create"),
    path('trainers/update/<str:pk>/', views.trainer_update, name="trainer_update"),
    path('trainers/delete/<str:pk>/', views.trainer_delete, name="trainer_delete"),

    path('incomes/', views.incomes, name="incomes"),
    path('incomes/create/', views.income_create, name="income_create"),
    path('incomes/update/<str:pk>/', views.income_update, name="income_update"),
    path('incomes/delete/<str:pk>/', views.income_delete, name="income_delete"),

    path('expenses/', views.expenses, name="expenses"),
    path('expenses/create/', views.expense_create, name="expense_create"),
    path('expenses/update/<str:pk>/', views.expense_update, name="expense_update"),
    path('expenses/delete/<str:pk>/', views.expense_delete, name="expense_delete"),

    path(
    'password_reset/',
    auth_views.PasswordResetView.as_view(template_name='gyms/password/password_reset.html'), name="password_reset"
    ),
    path(
    'password_reset/done',
    auth_views.PasswordResetDoneView.as_view(template_name='gyms/password/password_reset_done.html'), name="password_reset_done"
    ),
    path(
    'password_reset/confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name='gyms/password/password_reset_confirm.html'), name="password_reset_confirm"
    ),
    path(
    'password_reset/complete',
    auth_views.PasswordResetCompleteView.as_view(template_name='gyms/password/password_reset_complete.html'), name="password_reset_complete"
    ),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
