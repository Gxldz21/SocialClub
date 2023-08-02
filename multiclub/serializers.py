from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from .models import *


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('__all__')

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('__all__')

class PostSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(slug_field='slug',queryset=Group.objects.all(),required=False, allow_null=True)
    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'pub_date', 'group', 'tags')

