from django.urls import path
from . import views


app_name = 'posts'
urlpatterns = [
    path('', views.timeline, name='timeline'),
    path('post_id=<int:post_id>/', views.view_post, name='view_post'),
    path('post_id=<int:post_id>/send_report/', views.send_post_report, name='send_post_report'),
    path('post_id=<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('post_id=<int:post_id>/delete_comment_id=<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('post_id=<int:post_id>/ocultar/', views.ocultar_post, name='ocultar_post'),
    ]