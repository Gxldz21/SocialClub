from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    text = models.CharField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', blank=True, null=True, related_name='groups', on_delete=models.CASCADE)
    image = models.ImageField('Картинка', upload_to='posts/', blank=True)


class Group(models.Model):
    title = models.CharField(max_length=500)
    slug = models.CharField(max_length=500)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.title


class Comment(models.Model):
    com_date = models.DateTimeField(auto_now_add=True)
    com_author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='posts', on_delete=models.CASCADE)
    com_text = models.CharField(max_length=500)


class Follow(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
