from django.contrib.auth.models import User
from django.urls import reverse
from .models import Task
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
import json

class TaskModelTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_data = {
            'username': 'user',
            'email': 'test@example.com',
            'password': '1234567890!',
            'password_confirmed': '1234567890!',
        }

        self.created_user = User.objects.create_user(
            username='user', email='test@example.com', password='1234567890!'
        )
        
        refresh = RefreshToken.for_user(self.created_user)
        self.access_token = str(refresh.access_token)
        self.refresh_token = str(refresh)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")


    def test_create_task(self):
        response = self.client.post(reverse('task-list'), {
            'title': 'Test Task',
            'desc': 'Description of the test task',
            'status': 'NEW',
            'priority': 'MEDIUM'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Task')

    def test_update_task_status(self):
        task = Task.objects.create(
            title='Existing Task',
            desc='Task description',
            status='NEW',
            priority='LOW',
            user=self.created_user
        )
        url = reverse('task-detail', args=[task.id])
        response = self.client.patch(url, 
            {'status': 'IN PROGRESS'},)
        task.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(task.status, 'IN PROGRESS')

    def test_update_task_priority(self):
        task = Task.objects.create(
            title='Priority Task',
            desc='Task description',
            status='NEW',
            priority="LOW",
            user=self.created_user
        )
        url = reverse('task-detail', args=[task.id])
        response = self.client.patch(url, {
            "priority": "HIGH"},)
        task.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(task.priority, 'HIGH')

    def test_invalid_task_creation(self):
        response = self.client.post(reverse('task-list'), {
            'title': '',
            'desc': 'Description without title',
            'status': 'INVALID_STATUS',
            'priority': 'MEDIUM'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Task.objects.count(), 0)