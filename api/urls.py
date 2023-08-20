from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as views_token
from rest_framework.routers import SimpleRouter, DefaultRouter
from . import views
from .views import *

app_name = 'api'

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('group', GroupViewSet, basename='group')
comments_router = DefaultRouter()
comments_router.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('api/v1/api-token-auth/', views_token.obtain_auth_token),
    path('api/v1/', include(router.urls)),
    path('api/v1/<int:post_id>/', include(comments_router.urls)),

]
