from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.show_all_users, name='show_all_users'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', views.current_user_profile, name='current_user_profile'),
    path('privacidade/', views.privacidade, name='privacidade'),
    path('privacidade/tirar_post_id=<int:post_id>_ocultado', views.tirar_post_ocultado, name='tirar_post_ocultado'),
    path('privacidade/tirar_user_id=<int:user_id>_ocultado', views.tirar_user_ocultado, name='tirar_user_ocultado'),
    path('privacidade/tirar_user_id=<int:user_id>_bloqueado', views.tirar_user_bloqueado, name='tirar_user_bloqueado'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/user_id=<int:user_id>/',views.user_profile, name='user_profile'),
    path('profile/user_id=<int:user_id>/send_report',views.send_report, name='send_report'),
    path('profile/user_id=<int:user_id>/ocultar',views.ocultar_user, name='ocultar_profile'),
    path('profile/user_id=<int:user_id>/bloquear',views.bloquear_user, name='bloquear_profile'),
    ]
