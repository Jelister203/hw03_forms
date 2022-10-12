from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    verbouse_name = 'Группы'

    def __str__(self):
        return f"Группа {self.title}"


class Post(models.Model):
    verbouse_name = 'Посты'
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,
                               related_name='posts',
                               on_delete=models.CASCADE)
    group = models.ForeignKey(Group,
                              blank=True,
                              related_name='posts',
                              null=True,
                              on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-pub_date']
