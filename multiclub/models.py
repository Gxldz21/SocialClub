from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tags(models.Model):
    name = models.CharField(max_length=100)


class Post(models.Model):
    title = models.CharField(max_length=200, null=False)
    text = models.CharField(max_length=5000)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', blank=True, null=True, related_name='groups', on_delete=models.CASCADE)
    image = models.ImageField('Картинка', upload_to='posts/', blank=True)
    tags = models.ManyToManyField(Tags, through='PostTags')


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
    tags = models.ForeignKey(Tags, related_name='tags', on_delete=models.CASCADE)
