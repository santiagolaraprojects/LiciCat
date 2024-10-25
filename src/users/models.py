# Create your models here.
from sqlite3 import IntegrityError
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import ValidationError
from licitacions.models import Localitzacio
from users import choices
from licitacions.models import Licitacio

class Rating(models.Model):
    evaluating_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='evaluating_user')
    evaluated_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='evaluated_user')
    value = models.IntegerField(null=True)



class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    mesage = models.CharField(max_length=150, choices=choices.notifications, null=True)
    licitacio = models.ForeignKey(Licitacio, on_delete=models.CASCADE, null=True, blank=True, related_name='licitacio_afectada')
    nom_licitacio = models.CharField(max_length=150, null=True)
    username = models.CharField(max_length=150, null=True)

    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('Email can not be null.')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        try:
            user.save(using=self._db)
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e) and 'username' in str(e):
                raise ValueError('Username already exists.')
            elif 'UNIQUE constraint' in str(e) and 'email' in str(e):
                raise ValueError('Email already exists.')
            else:
                raise e
        return user
      
class CustomUser(AbstractUser):
    #custom fields
    email = models.EmailField(verbose_name='email address', unique=True, blank=False)
    username = models.TextField(max_length=30, unique=True, blank=False)
    name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=310, blank=True)
    CIF = models.TextField( max_length=10, null=True)
    tipus_id = models.TextField(null=True)
    descripcio = models.TextField(null=True)
    localitzacio = models.TextField(null=True)
    cp = models.TextField(null=True)
    idioma = models.TextField(null=True)
    
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    


class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='follower')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='following')
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'], name='unique_follow'
            )
        ]
