from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tags(models.Model):
    tags = models.CharField(max_length=100)

class Post(models.Model):
    text = models.CharField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', blank=True, null=True, related_name='groups', on_delete=models.CASCADE)
    image = models.ImageField('Картинка', upload_to='posts/', blank=True)
    tags = models.ManyToManyField(Tags, through='PostTags')

    def create(self, validated_data):
        # Если в исходном запросе не было поля achievements
        if 'tags' not in self.initial_data:
            # То создаём запись о котике без его достижений
            post = Post.objects.create(**validated_data)
            return post

        # Иначе делаем следующее:
        # Уберём список достижений из словаря validated_data и сохраним его
        achievements = validated_data.pop('tags')
        # Сначала добавляем котика в БД
        post = Post.objects.create(**validated_data)
        # А потом добавляем его достижения в БД
        for achievement in tags:
            current_achievement, status = Achievement.objects.get_or_create(
                **achievement)
            # И связываем каждое достижение с этим котиком
            AchievementCat.objects.create(
                achievement=current_achievement, cat=cat)
        return cat

class Group(models.Model):
    title = models.CharField(max_length=500)
    slug = models.CharField(max_length=500)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.slug


class Comment(models.Model):
    com_date = models.DateTimeField(auto_now_add=True)
    com_author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='posts', on_delete=models.CASCADE)
    com_text = models.CharField(max_length=500)


class Follow(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)


class PostTags(models.Model):
    post = models.ForeignKey(Post, related_name='post', on_delete=models.CASCADE)
    tags = models.ForeignKey(Tags, related_name='tag', on_delete=models.CASCADE)
