from django.core.exceptions import ValidationError
from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .permissions import *
from .pagination import *

from multiclub.models import *

from .serializers import *


# def get_object(self):
#     obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
#     self.check_object_permissions(self.request, obj)
#     return obj

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('pub_date')
    serializer_class = PostSerializer
    permission_classes = (IsOwnerPostOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$text',)

    def perform_create(self, serializer):
        author = User.objects.filter(username=self.request.user)[0]
        serializer.save(author=author)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('title')
    serializer_class = GroupSerializer
    permission_classes = (IsOwnerPostOrReadOnly,)
    pagination_class = CustomPagination


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = (IsOwnerPostOrReadOnly,)
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        author = User.objects.filter(username=self.request.user)[0]
        serializer.save(com_author=author, post=post)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post=post_id)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsOwnerPostOrReadOnly,)

    pagination_class = CustomPagination

    def get_queryset(self):
        followings = Follow.objects.filter(user=self.request.user)
        queryset = followings
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
