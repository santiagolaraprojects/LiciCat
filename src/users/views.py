from rest_framework import generics
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes, api_view, action
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import json
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import views
from rest_framework import mixins
from rest_framework import generics
from users.models import Follow
from licitacions.models import *
from users.serializers import *
from users.permissions import IsCreationOrIsAuthenticated
from users.models import *

from django.db.models import Avg

# List all the users and register, delete and update the own user 
class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsCreationOrIsAuthenticated,)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action == 'list':
            return UserPreviewSerializer
        if self.action == 'put':
            return UserProfileEditSerializer
        if self.action == 'delete':
            return UserProfileSerializer
        return UserSerializer
    
    def get_queryset(self):
        print('he entrado')
        queryset = CustomUser.objects.all()

        prefix = self.request.query_params.get('prefix')
        if prefix is not None:
            queryset = queryset.filter(lloc_execucio__nom__icontains=prefix)
        return queryset

    
    @action(methods=['put'], detail=False)
    def put(self, request, format=None):
        user = request.user
        serializer = UserProfileEditSerializer(user, data=request.data, partial=True)
        data_cif = json.dumps(request.data.get('CIF')).strip('"').strip()
        print(data_cif)
        if (len(data_cif) == 9 and not data_cif[0].isnumeric() and not data_cif[8].isnumeric() and data_cif[1:7].isnumeric()):
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'El valor del nuevo CIF introducido es incorrecto'} , status=status.HTTP_400_BAD_REQUEST)
        
    
    @action(methods=['delete'], detail=False)
    def delete(self, request, format=None):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OwnUserView(APIView):
    #Autentificacion
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, format=None):
        serializer = UserProfileEditSerializer(request.user)
        return Response(serializer.data)

# List one user
class UserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


# Follow Users Views
class FollowView(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)
    
    def post(self,request, pk):
        User = get_user_model()
        follower = request.user
        following = get_object_or_404(User, id=pk)
        follows = Follow.objects.filter(follower=follower, following=following).first()
        if follows:
            follows.delete()
            response_data = {'following': following.email, 'user': follower.email, 'action': 'unfollowed', 'success': True}
        else:
            follows = Follow(follower=follower, following=following)
            follows.save()
            try:
                Notification.objects.create(
                    user = following,
                    mesage = 'Nuevo Seguidor',
                    username = follower.username
                )
            except:
                return Response({"error":"Error al generar la notificacion"})
            response_data = {'following': following.email, 'user': follower.email, 'action': 'followed', 'success': True}
        return JsonResponse(response_data)
    
class ListFollowing(generics.ListAPIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)
    serializer_class = UserPreviewSerializer

    def get_queryset(self):
        user = self.request.user
        following = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
        User = get_user_model()
        return User.objects.filter(id__in=following)
    
class ListFollowers(generics.ListAPIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)
    serializer_class = UserPreviewSerializer

    def get_queryset(self):
        user = self.request.user
        followers = Follow.objects.filter(following=user).values_list('follower_id', flat=True)
        User = get_user_model()
        return User.objects.filter(id__in=followers)

# User Preferences View  
class Add_to_preferences(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def post(self, request):
        user = request.user

        tipus_contracte_ids = request.query_params.get('tipus_contracte')
        PreferenceTipusContracte.objects.filter(user=user).delete()
        if tipus_contracte_ids is not None and tipus_contracte_ids != "":
            tipus_contracte_ids = [int(id) for id in tipus_contracte_ids.split(',')]
            for tipus_contracte_id in tipus_contracte_ids:
                tipus_contracte = get_object_or_404(TipusContracte, id=tipus_contracte_id)
                preference_tp = PreferenceTipusContracte(user=user, tipus_contracte=tipus_contracte)
                try:
                    preference_tp.save()
                except:
                    pass

        ambit_ids = request.query_params.get('ambit')
        PreferenceAmbit.objects.filter(user=user).delete()
        if ambit_ids is not None and ambit_ids != "":
            ambit_ids = [int(id) for id in ambit_ids.split(',')]
            for ambit_id in ambit_ids:
                ambit = get_object_or_404(Ambit, codi=ambit_id)
                preference_amb = PreferenceAmbit(user=user, ambit=ambit)
                try:
                    preference_amb.save()
                except:
                    pass
        
        pressupost_min = request.query_params.get('pressupost_min')
        pressupost_max = request.query_params.get('pressupost_max')
        PreferencePressupost.objects.filter(user=user).delete()
        if pressupost_min != "-1" or pressupost_max != "-1":
            print("bk 1")
            if pressupost_max == "-1":
                print("bk 2")
                pressupost_max = None
            if pressupost_min == "-1":
                print("bk 3")
                pressupost_min = None
            preference_press = PreferencePressupost(user=user, pressupost_min=pressupost_min, pressupost_max=pressupost_max)
            try:
                preference_press.save()
            except:
                pass
        
        privades = request.query_params.get('privades')
        print(privades)
        publiques = request.query_params.get('publiques')
        print(publiques)
        PreferenceTipusLicitacio.objects.filter(user=user).delete()
        if privades is not None or publiques is not None:
            if privades is None:
                privades = False
            if publiques is None:
                publiques = False
            preference_tipus_lic = PreferenceTipusLicitacio(user=user, privades=privades, publiques=publiques)
            try:
                preference_tipus_lic.save()
            except:
                pass

        return JsonResponse({'status': 'ok'})
    
    def get(self, request):
        user = request.user

        tipus_contracte_preferences = PreferenceTipusContracte.objects.filter(user=user)
        tipus_contracte_data = [{"id": p.tipus_contracte.id, "name": str(p.tipus_contracte)} for p in tipus_contracte_preferences]

        ambit_preferences = PreferenceAmbit.objects.filter(user=user)
        ambit_data = [{"id": p.ambit.codi, "name": p.ambit.nom} for p in ambit_preferences]

        pressupost_preference = PreferencePressupost.objects.filter(user=user).first()
        pressupost_data = {"pressupost_min": pressupost_preference.pressupost_min if pressupost_preference else None,
                           "pressupost_max": pressupost_preference.pressupost_max if pressupost_preference else None}

        tipus_lic_preference = PreferenceTipusLicitacio.objects.filter(user=user).first()
        tipus_lic_data = {"privades": tipus_lic_preference.privades if tipus_lic_preference else False,
                          "publiques": tipus_lic_preference.publiques if tipus_lic_preference else False}

        return JsonResponse({"tipus_contracte": tipus_contracte_data,
                             "ambit": ambit_data,
                             "pressupost": pressupost_data,
                             "tipus_licitacio": tipus_lic_data})
        
class RatingCreateView(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def post(self, request):
        evaluating_user = request.POST.get('evaluating_user')
        evaluated_user = request.POST.get('evaluated_user')
        value = request.POST.get('value')

        user_from = get_object_or_404(CustomUser, email=evaluating_user)
        user_to = get_object_or_404(CustomUser, email=evaluated_user)

        # Verificar si existe una valoración previa y eliminarla si es el caso
        try:
            previous_rating = Rating.objects.get(
                evaluating_user=user_from, evaluated_user=user_to
            )
            previous_rating.delete()
        except Rating.DoesNotExist:
            pass

        rating = Rating(evaluating_user=user_from, evaluated_user=user_to, value=value)
        rating.save()

        return JsonResponse({'success': evaluating_user + 'ha valorado con un ' + value + ' a ' + evaluated_user})
    
    def get(self, request):
        evaluating_user = request.GET.get('evaluating_user')
        evaluated_user = request.GET.get('evaluated_user')

        try:
            rating = Rating.objects.get(
                evaluating_user__email=evaluating_user,
                evaluated_user__email=evaluated_user
            )
            value = rating.value

            return JsonResponse({'value': value})
        except Rating.DoesNotExist:
            return JsonResponse({'value': 0})


class RatingAverageView(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)
    
    def get(self, request):
        user_email = request.GET.get('evaluated_user')

        user = get_object_or_404(CustomUser, email=user_email)

        average = Rating.objects.filter(evaluated_user=user).aggregate(Avg('value'))['value__avg']
        if average is not None:
            average = round(average, 2)

        return JsonResponse({'average_rating': average})

class NotificationsList(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)
    
    def get(self, request):
        if request.user.is_authenticated:
            notifications = Notification.objects.filter(user=request.user)
            NotificationSerializer(notifications, many = True)
            return Response(NotificationSerializer(notifications, many = True).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

class BuscarPorNombre(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def post(self, request):
        try:
            users = CustomUser.objects.filter(username__startswith=request.data.get("prefix"))
        except User.DoesNotExist:
            return Response({'error': 'No hay usuarios que comiencen por el prefijo'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# # UserSerializer