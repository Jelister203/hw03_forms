from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    class Meta:
        verbose_name = 'Группы'
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return f"Группа {self.title}"


class Post(models.Model):
    class Meta:
        verbose_name = 'Посты'
        ordering = ['-pub_date']
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
