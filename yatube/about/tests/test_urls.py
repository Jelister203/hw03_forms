from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest = Client()

    def test_static_pages(self):
        about_response = self.guest.get('/about/author/')
        tech_response = self.guest.get('/about/tech/')
        self.assertEqual(about_response.status_code, 200)
        self.assertEqual(tech_response.status_code, 200)
