from django.urls import path
from . import views

urlpatterns = [
    # Auth URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Student Portal URLs
    path('', views.student_list, name='student_list'),
    path('add/', views.student_create, name='student_create'),
    path('edit/<int:pk>/', views.student_update, name='student_update'),
    path('delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('seed/', views.seed_sample_data, name='seed_sample_data'),
]
