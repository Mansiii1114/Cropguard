from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('recommend/', views.recommend_view, name='recommend'),
    path('disease/', views.disease_view, name='disease'),
    path('history/', views.history_view, name='history'),
    path('library/', views.library_view, name='library'),
    path('library/<str:crop_name>/', views.crop_detail_view, name='crop_detail'),
]
