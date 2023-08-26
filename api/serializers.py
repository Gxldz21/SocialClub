from rest_framework import validators
from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from multiclub.models import *


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        source='author'
    )
    def validate_following(self, value):
        user = self.context['request'].user
        if user == value:
            raise serializers.ValidationError(
                "Попытка подписатся на самого себя.")
        return value

    class Meta:
        fields = 'user','following'
        model = Follow
        validators = [
            validators.UniqueTogetherValidator(queryset=Follow.objects.all(),
                                               fields=('user', 'author'))
        ]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('__all__')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('name',)


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(source='com_author', slug_field='username', queryset=User.objects.all(),
                                          required=False,
                                          allow_null=True)
    date = serializers.DateTimeField(source='com_date', required=False)
    text = serializers.CharField(source='com_text', max_length=500)

    class Meta:
        model = Comment
        fields = ('id', 'date', 'text', 'author', 'post_id')


class PostSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, required=False, allow_null=True)
    character_quantity = serializers.SerializerMethodField()
    publication_date = serializers.DateTimeField(source='pub_date', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'image', 'publication_date', 'group', 'tags', 'character_quantity')
        read_only_fields = ('author',)

    def get_character_quantity(self, obj):
        return len(obj.text)

    def create(self, validated_data):
        if 'tags' not in self.initial_data:
            post = Post.objects.create(**validated_data)
            return post

        tags = validated_data.pop('tags')
        post = Post.objects.create(**validated_data)
        for tag in tags:
            current_tag, status = Tags.objects.get_or_create(
                **tag)
            PostTags.objects.create(
                tags=current_tag, post=post)
        return post

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['author'] = instance.author.username
        if self.context['request'].method == 'GET':
            if data['group'] is not None:
                data['group'] = instance.group.title
        return data
