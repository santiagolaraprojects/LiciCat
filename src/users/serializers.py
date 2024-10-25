from rest_framework import serializers

from users.models import CustomUser
from django.http import JsonResponse
from rest_framework import status
from .models import Follow, Notification
from django.contrib.auth import get_user_model
from rest_framework import serializers

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        User = get_user_model()
        model = User
        fields = ('id', 'username', 'password', 'email', 'name')
        
    def create(self, validated_data):
        User = get_user_model()
        try:
            user = User.objects.create_user(**validated_data)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        print("Usuario creado correctamente")
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        User = get_user_model()
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'name')
        extra_kwargs = {'password': {'write_only': True, 'required': False}}
    def create(self, validated_data):
        User = get_user_model()
        try:
            user = User.objects.create_user(**validated_data)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        print("Usuario creado correctamente")
        return user

# Serializer to list the Users
class UserPreviewSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        User = get_user_model()
        model = User
        fields = ('id', 'username', 'name', 'following')
        
    def get_following(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                Follow.objects.get(follower=user, following=obj)
                return True
            except Follow.DoesNotExist:
                pass
        return False
  
# Serializer to view the User Profile  
class UserProfileSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        User = get_user_model()
        model = User
        fields = ('id', 'username', 'email', 'name', 'descripcio', 'phone', 'localitzacio',  'CIF', 'tipus_id', 'cp', 'idioma', 'following')
        
    def get_following(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                Follow.objects.get(follower=user, following=obj)
                return True
            except Follow.DoesNotExist:
                pass
        return False
    
# Serializer to edit the User Profile  
class UserProfileEditSerializer(serializers.ModelSerializer):

    class Meta:
        User = get_user_model()
        model = User
        fields = ('id', 'username', 'email', 'name', 'descripcio', 'phone', 'localitzacio', 'CIF', 'tipus_id', 'cp', 'idioma')
        
    def get_following(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                Follow.objects.get(follower=user)
                return True
            except Follow.DoesNotExist:
                pass
        return False
    
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
