from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .permissions import *

from multiclub.models import *

from multiclub.serializers import *


# def get_object(self):
#     obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
#     self.check_object_permissions(self.request, obj)
#     return obj

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerPostOrReadOnly,)

    def perform_create(self, serializer):
        author = User.objects.filter(username=self.request.user)[0]
        serializer.save(author=author)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsOwnerPostOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = (IsOwnerPostOrReadOnly,)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        author = User.objects.filter(username=self.request.user)[0]
        serializer.save(com_author=author, post=post)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post=post_id)
