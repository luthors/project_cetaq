import json
from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker

class TestSetUp(APITestCase):
    def setUp(self):
        from apps.users.models import User
        faker = Faker()
        
        self.login_url = '/login/'
        self.user = User.objects.create_superuser(
            name='test',
            email= faker.email(),
            password='testtest',
            last_name='test',
        )
        
        response = self.client.post(
            self.login_url,
            data={
                'email': self.user.email,
                'password': 'testtest'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        return super().setUp()
    
    def test_setup(self):
        print('Comprobando creación de DB, ingreso a login y generación del token')
        print('Token: ', self.token)
        print('User: ', self.user)
        