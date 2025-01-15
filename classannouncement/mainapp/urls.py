from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_login, name='redirect-to-login'),
    path('login/', views.login_view, name='login'),
    path('user/<int:user_id>/', views.user_profile, name='user-profile'),
    path('board/', views.global_chat, name='global-chat'),
    path('board/post/', views.create_global_message, name='create-global-message'),
    path('section/<int:section_id>/', views.section_chat, name='section-chat'),
    path('section/<int:section_id>/post/', views.create_section_message, name='create-section-message'),
]