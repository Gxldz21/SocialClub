from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter

from .views import *

app_name = 'social'

urlpatterns = [
    path('', views.index, name='main'),
    path('group/<slug:slug>/',views.group_posts, name='group'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('create_post/', views.new_post, name='create'),
    path('posts/<int:post_id>/edit', views.update_post, name='update'),
    path('posts/<int:post_id>/del', views.delete_post, name='delete'),
    path('posts/<int:post_id>/comment', views.comment, name='comment'),
    path('profile/<str:username>/follow', views.follow, name='follow'),
    path('posts/<int:post_id>/like', views.like_post, name='like'),
    path('subscribe/', views.sub, name='sub'),
    path('posts/tags/<str:tag_name>', views.post_tags, name='tag'),
    path('settings/<str:username>/', views.settings_user, name='settings'),
    path('settings/<str:username>/del', views.delete_image, name='del_image'),
    path('comment/<int:com_id>/del', views.delete_com, name='com_del'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )