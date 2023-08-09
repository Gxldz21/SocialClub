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
        fields = ('name',)

class PostSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(slug_field='slug',queryset=Group.objects.all(),required=False, allow_null=True)
    tags = TagsSerializer(many=True)
    character_quantity = serializers.SerializerMethodField()
    publication_date = serializers.DateTimeField(source='pub_date', read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'publication_date', 'group', 'tags', 'character_quantity')

    def get_character_quantity(self, obj):
        return len(obj.text)

    def create(self, validated_data):
        # Если в исходном запросе не было поля achievements
        if 'tags' not in self.initial_data:
            # То создаём запись о котике без его достижений
            post = Post.objects.create(**validated_data)
            return post

        # Иначе делаем следующее:
        # Уберём список достижений из словаря validated_data и сохраним его
        tags = validated_data.pop('tags')
        # Сначала добавляем котика в БД
        post = Post.objects.create(**validated_data)
        # А потом добавляем его достижения в БД
        for tag in tags:
            current_tag, status = Tags.objects.get_or_create(
                **tag)
            # И связываем каждое достижение с этим котиком
            PostTags.objects.create(
                tags=current_tag, post=post)
        return post

