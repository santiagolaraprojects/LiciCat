from decimal import Decimal
from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Perfil, CustomUser
from licitacions.models import Localitzacio
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
        localitzacio = Localitzacio.objects.create(
            nom = 'localitzacio_test',
            longitud = 1.001,
            latitud = 1.05
        )
        self.perfil = Perfil.objects.create(
            CIF = 'B1234567C',
            tipus_id = 'id_type_test',
            user = user,
            descripcio = 'is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry',
            localitzacio = localitzacio,
            cp = 'aaaaaaaaa',
            telefon = '660616062',
            idioma = 'castellano'
        )


    def test_creadora_perfil(self):
        """Los campos de los parametros deberian coincidir con los dela creadora"""
        perfil = Perfil.objects.get(CIF = 'B1234567C')
        user = perfil.user
        localitzacio = perfil.localitzacio 
        self.assertEqual(perfil.CIF, 'B1234567C')
        self.assertEqual(user.username, 'username_test')
        self.assertEqual(user.password, '1234')
        self.assertEqual(user.email, 'a@a.com')
        self.assertEqual(localitzacio.nom, 'localitzacio_test')
        self.assertEqual(localitzacio.longitud, Decimal('1.001'))
        self.assertEqual(localitzacio.latitud, Decimal('1.05'))
        self.assertEqual(perfil.tipus_id, 'id_type_test')
        self.assertEqual(perfil.descripcio, 'is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry')
        self.assertEqual(perfil.cp, 'aaaaaaaaa')
        self.assertEqual(perfil.telefon, '660616062')
        self.assertEqual(perfil.idioma, 'castellano')

    def test_editar_perfil_CIF_not_exists(self):
        """Deberia retornar 404, ya que el CIF no corresponde con el que creamos en el setUp"""
        url = 'http://127.0.0.1:8000/editProfile/CIFMALO'
        data = {
            'CIF': 'CIFMALO',
            'tipus_id': 'id_type_test',
            'descripcio': 'is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry',
            'cp': 'aaaaaaaaa',
            'telefon': '660616062',
            'idioma': 'castellano'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_editar_perfil_CIF_too_long(self):
        """Deberia retornar 400, ya que el CIF no es valido"""
        url = 'http://127.0.0.1:8000/api/editProfile/B1234567C/'
        data = {
            'CIF': 'B1234567CX',
            'tipus_id': 'id_type_test',
            'descripcio': 'is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry',
            'cp': 'aaaaaaaaa',
            'telefon': '660616062',
            'idioma': 'castellano'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_editar_perfil_CIF_invalid(self):
        """Deberia retornar 400, ya que el CIF tiene un caracter en la zona de numeros"""
        url = 'http://127.0.0.1:8000/api/editProfile/B1234567C/'
        data = {
            'CIF': 'B12345S7C',
            'tipus_id': 'id_type_test',
            'descripcio': 'is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry',
            'cp': 'aaaaaaaaa',
            'telefon': '660616062',
            'idioma': 'castellano'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_editar_perfil_CIF_too_short(self):
        """Deberia retornar 400, ya que el CIF es demasiado corto"""
        url = 'http://127.0.0.1:8000/api/editProfile/B1234567C/'
        data = {
            'CIF': 'B123457C',
            'tipus_id': 'id_type_test',
            'descripcio': 'is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry',
            'cp': 'aaaaaaaaa',
            'telefon': '660616062',
            'idioma': 'castellano'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_editar_perfil_valid(self):
        """Deberia retornar 200, realizar los cambios indicados a por la peticion PUT"""
        url = 'http://127.0.0.1:8000/api/editProfile/B1234567C/'
        data = {
            'CIF': 'B1234567C',
            'tipus_id': 'id_new',
            'descripcio': 'nuevadesc',
            'cp': 'bbbbbb',
            'telefon': '+34666666666',
            'idioma': 'english'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        perfil_actualizado = Perfil.objects.get(CIF=self.perfil.CIF)
        self.assertEqual(perfil_actualizado.CIF, 'B1234567C')
        self.assertEqual(perfil_actualizado.tipus_id, 'id_new')
        self.assertEqual(perfil_actualizado.descripcio, 'nuevadesc')
        self.assertEqual(perfil_actualizado.cp, 'bbbbbb')
        self.assertEqual(perfil_actualizado.telefon, '+34666666666')        
        self.assertEqual(perfil_actualizado.idioma, 'english')

class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'usuariprova@gmail.com',
            'username': 'usuari1',
            'password': '12345678t',
            'name': 'NomUsuari',
        }

    def test_creadora_usuari(self):
        response = self.client.post('/api/users/', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CustomUser.objects.count(), 1)
        user = CustomUser.objects.last()
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.name, self.user_data['name'])
        self.assertTrue(user.check_password(self.user_data['password']))

    def test_create_user_without_email(self):
        """Debe lanzar una excepción al intentar crear un usuario sin email"""
        with self.assertRaises(ValueError) as cm:
            CustomUser.objects.create_user(email=None, username='username',password='password')
        self.assertEqual(str(cm.exception), 'Email can not be null.')

    def test_create_user_with_existing_email(self):
        """Debe lanzar una excepción al intentar crear un usuario con un email existente"""
        CustomUser.objects.create_user(
            email=self.user_data['email'], 
            username='username',
            password='password'
        )
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                email=self.user_data['email'], 
                username='username2',
                password='password2'
            )

    def test_create_user_with_existing_username(self):
        CustomUser.objects.create_user(
            email='email1', 
            username='username',
            password='password'
        )
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
               email='email1', 
                username='username',
                password='password2'
            )