from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Perfil, CustomUser
from licitacions.models import ListaFavorits, Licitacio
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

# Create your tests here.

class EditUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = CustomUser.objects.create(
            username = 'username_test',
            password = '1234',
            email = 'a@a.com'    
        )
        licitacio = Licitacio.objects.create( 
            id = 123400000
        )
        ListaFavorits.objects.create(
            user = user,
            licitacio = licitacio    
        )


    def test_eliminar_entrada(self):
        """Deberia eliminarse la entrada de la relacion"""
        url = 'http://127.0.0.1:8000/api/unfollow/' + 123400000
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
