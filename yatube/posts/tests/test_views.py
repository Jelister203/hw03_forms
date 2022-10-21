from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from datetime import datetime
from posts.models import Post, Group

User = get_user_model()


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username='author')
        group = Group.objects.create(
            title='Группа',
            slug='slug',
            description='Описание группы',
        )
        Post.objects.create(
            text='Пост',
            pub_date=datetime.now(),
            author=cls.author,
            group=group,
        )
        Post.objects.create(
            text='Пост без группы',
            author=cls.author,
        )

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(self.author)
        self.unauth_client = Client()

    def test_correct_template(self):
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list'): 'posts/group_list.html',
            reverse('posts:profile'): 'posts/profile.html',
            reverse('posts:post_detail'): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit'): 'posts/create_post.html',
        }

    def test_correct_context(self):
        pass
