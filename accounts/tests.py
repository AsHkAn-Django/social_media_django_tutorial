from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from accounts.models import Follow
from myApp.models import Post


User = get_user_model()


class AccountAPIViewTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='user1pass')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='user2pass')
        self.client = APIClient()

    def test_user_list_admin_only(self):
        url = reverse('accounts_api:users')

        # Not authenticated
        res = self.client.get(url)
        # This should get 403 but because redirects user to login page it gets 302
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # Logged in as regular user
        self.client.login(username='user1', password='user1pass')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # Logged in as admin
        self.client.login(username='admin', password='adminpass')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('users', res.data)

    def test_follow_user(self):
        self.client.login(username='user1', password='user1pass')
        url = reverse('accounts_api:follows')
        res = self.client.post(url, {'user': self.user2.username})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 1)

    def test_unfollow_user(self):
        Follow.objects.create(follower=self.user1, user=self.user2)
        self.client.login(username='user1', password='user1pass')
        url = reverse('accounts_api:follows')
        res = self.client.post(url, {'user': self.user2.username})
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Follow.objects.count(), 0)

    def test_cannot_follow_self(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('accounts_api:follows')
        res = self.client.post(url, {'user': self.user1.username})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        error_message = res.data.get('Error')
        if error_message:
            self.assertIn("can't follow yourself", error_message.lower())
        else:
            self.fail(f"Expected 'Error' in response but got: {res.data}")

    def test_get_follow_list(self):
        Follow.objects.create(follower=self.user1, user=self.user2)
        self.client.login(username='user1', password='user1pass')
        url = reverse('accounts_api:follows')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('follows', res.data)

    def test_feed_only_followed_posts(self):
        Follow.objects.create(follower=self.user1, user=self.user2)
        Post.objects.create(title="user2's post", body='body', author=self.user2)
        Post.objects.create(title="admin post", body="body", author=self.admin)

        self.client.login(username='user1', password='user1pass')
        url = reverse('accounts_api:feeds')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['author'], 'user2')

    def test_feed_requires_authentication(self):
        url = reverse('accounts_api:feeds')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
