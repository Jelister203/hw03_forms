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
        cls.group = Group.objects.create(
            title='Группа',
            slug='slug',
            description='Описание группы',
        )
        Post.objects.create(
            text='Пост',
            pub_date=datetime.now(),
            author=cls.author,
            group=cls.group,
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

            (reverse('posts:group_list', kwargs={'slug': 'slug'})):
                'posts/group_list.html',

            (reverse('posts:profile', kwargs={'username': 'author'})):
                'posts/profile.html',

            (reverse('posts:post_detail', kwargs={'post_id': 1})): 'posts/post_detail.html',

            (reverse('posts:post_edit', kwargs={'post_id': 1})): 'posts/create_post.html',

            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.auth_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_correct_context(self):
        pass
