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
    path('subscribe/', views.sub, name='sub'),
    # path('tags/<str:tag_name>', views.post_tags, name='tag')
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )