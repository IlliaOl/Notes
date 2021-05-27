from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser


class TestingAuth(TestCase):

    def setUp(self):
        self.client = Client()
        self.list_url = reverse('note_list')
        self.create_url = reverse('note_new')
        self.signup_url = reverse('login')
        self.login_url = reverse('signup')
        self.user = CustomUser.objects.create_user('test', 'test@gmail.com', 'password')
        self.user.save()

    def test_access_signup_page(self):
        response = self.client.get(self.signup_url)
        self.assertEquals(response.status_code, 200)

    def test_access_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)

    def test_login(self):

        user = CustomUser.objects.filter(username='test').first()
        user.is_active=True
        user.save()
        data = {
            'username':'test',
            'email':'test@gmail.com',
            'password':'password'
        }
        response = self.client.post(self.login_url, data, format='text\html')
        self.assertEquals(response.status_code, 200)

