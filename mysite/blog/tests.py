from django.test import TestCase, Client
from django.urls import reverse
from .models import Post, Subscriber
from .views import get_csrf_token, subscribe, create_blog, PostListView, PostDetailView
from django.contrib.auth.models import User


class PostListViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_existing_post(self):
        user = User.objects.create_user(username="testuser", password="testpassword")

        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="This is a test post",
            author=user,
        )

        response = self.client.get(reverse("post_detail", kwargs={"slug": post.slug}))
        self.assertEqual(response.status_code, 200)

    def test_get_nonexistent_post(self):
        response = self.client.get(
            reverse("post_detail", kwargs={"slug": "nonexistent"})
        )
        self.assertEqual(response.status_code, 404)


class GetCSRFTokenViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse("get_csrf_token"))
        self.assertEqual(response.status_code, 200)


class SubscribeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_valid_form(self):
        response = self.client.post(reverse("subscribe"), {"email": "test@example.com"})
        self.assertEqual(response.status_code, 200)

    def test_post_invalid_form(self):
        response = self.client.post(reverse("subscribe"), {"email": "invalid_email"})
        self.assertEqual(response.status_code, 400)


class CreateBlogViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_login(self.user)

    def test_post_valid_data(self):
        user = User.objects.create_user(username="testuser1", password="testpassword")
        self.client.force_login(user)

        response = self.client.post(
            reverse("create_blog"),
            {
                "title": "Test Blog Post",
                "slug": "test-blog-post",
                "content": "This is a test blog post.",
                "image": "test_image.jpg",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_post_invalid_data(self):
        user = User.objects.create_user(username="testuser2", password="testpassword")
        self.client.force_login(user)
