from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('habitat/<int:habitat_id>/', views.habitat_details, name='habitat_details'),
    path('amenities/<int:habitat_id>/', views.amenities_view, name='amenities'),
    path('compare/', views.compare, name='compare'),
    path('compare/result/', views.compare_result, name='compare_result'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='analyzer/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]
