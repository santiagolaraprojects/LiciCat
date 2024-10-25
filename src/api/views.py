from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework import generics
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


from publicdata.views import get_lloc_execucio
from licitacions.models import *
from users.models import *
from users.serializers import NotificationSerializer
from licitacions.serializers import *
from users.models import CustomUser
from users.serializers import UserSerializer, UserPreviewSerializer
from publicdata.views import get_data

class CronTests(generics.ListAPIView):

    def get(self, request):
           get_data()
           return Response(status=status.HTTP_200_OK)


class LicitacionsList(generics.ListAPIView):
    serializer_class = LicitacioPreviewSerializer

    def get_queryset(self):
        queryset = Licitacio.objects.all()

        localitzacio = self.request.query_params.get('lloc_execucio')
        if localitzacio is not None:
            queryset = queryset.filter(lloc_execucio__nom__icontains=localitzacio)

        pressupost_min = self.request.query_params.get('pressupost_min')
        if pressupost_min is not None:
            queryset = queryset.filter(pressupost__gte=pressupost_min)
        
        pressupost_max = self.request.query_params.get('pressupost_max')
        if pressupost_max is not None:
            queryset = queryset.filter(pressupost__lte=pressupost_max)
        
        tipus_contracte = self.request.query_params.get('tipus_contracte')
        if tipus_contracte is not None:
            queryset = queryset.filter(tipus_contracte_id=tipus_contracte)
        
        duracio_min = self.request.query_params.get('duracio_min')
        if duracio_min is not None:
            queryset = queryset.filter(duracio_contracte__gte=duracio_min)
        
        duracio_max = self.request.query_params.get('duracio_max')
        if duracio_max is not None:
            queryset = queryset.filter(duracio_contracte__lte=duracio_max)
        
        data_inici = self.request.query_params.get('data_inici')
        if data_inici is not None:
            queryset = queryset.filter(data_inici__gte=data_inici)

        data_fi = self.request.query_params.get('data_fi')
        if data_fi is not None:
            queryset = queryset.filter(data_fi__lte=data_fi)

        return queryset


class LicitacioDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        print("QUERYSET")
        queryset = None
        pk = self.kwargs.get('pk')
        licitacio_publica = LicitacioPublica.objects.filter(pk=pk)
        if licitacio_publica.exists():
            queryset = LicitacioPublica.objects.all()
        else:
            queryset = LicitacioPrivada.objects.all()
        return queryset

    def get_serializer_class(self):
        obj = self.get_object()
        pk = self.kwargs.get('pk')
        try:
            licitacio = Licitacio.objects.get(id = pk)
            if(licitacio.visualitzacions is None):
                licitacio.visualitzacions = 1
            else:
                licitacio.visualitzacions = licitacio.visualitzacions + 1
            licitacio.save()
        except Licitacio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if isinstance(obj, LicitacioPublica):
            print("entered lic pub serializer")
            return LicitacioPublicaDetailsSerializer
        elif isinstance(obj, LicitacioPrivada):
            print("entered lic priv serializer")
            return LicitacioPrivadaDetailsSerializer
        else:
            return self.serializer_class

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the instance is LicitacioPrivada
        if isinstance(instance, LicitacioPrivada):
            lloc_execucio = self.request.data.get('lloc_execucio')  # Assuming lloc_execucio is passed in the request data
            print(lloc_execucio)
            if lloc_execucio:
                # Check if the lloc_execucio exists in the database or create it
                localitzacio = get_lloc_execucio(lloc_execucio)
                #serializer.validated_data['lloc_execucio'] = localitzacio
            # Check if the user is authenticated and the owner of the LicitacioPrivada
            if request.user.is_authenticated and request.user == instance.user:
                return super().update(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the instance is LicitacioPrivada
        if isinstance(instance, LicitacioPrivada):
            # Check if the user is authenticated and the owner of the LicitacioPrivada
            if request.user.is_authenticated and request.user == instance.user:
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class LicitacionsPubliquesList(generics.ListAPIView):
    serializer_class = LicitacioPublicaPreviewSerializer
    
    def get_queryset(self):
        queryset = LicitacioPublica.objects.all()

        localitzacio = self.request.query_params.get('lloc_execucio')
        if localitzacio is not None:
            queryset = queryset.filter(lloc_execucio__nom__icontains=localitzacio)

        pressupost_min = self.request.query_params.get('pressupost_min')
        if pressupost_min is not None:
            queryset = queryset.filter(pressupost__gte=pressupost_min)
        
        pressupost_max = self.request.query_params.get('pressupost_max')
        if pressupost_max is not None:
            queryset = queryset.filter(pressupost__lte=pressupost_max)
        
        ambit = self.request.query_params.get('ambit')
        if ambit is not None:
            queryset = queryset.filter(ambit__nom__icontains=ambit)
            #queryset = queryset.filter(ambit_id=ambit)

        departament = self.request.query_params.get('departament')
        if departament is not None:
            queryset = queryset.filter(departament__nom__icontains=departament)
            #queryset = queryset.filter(departament_id=departament)

        organ = self.request.query_params.get('organ')
        if organ is not None:
            queryset = queryset.filter(organ__nom__icontains=organ)
            #queryset = queryset.filter(organ_id=organ)
        
        tipus_contracte = self.request.query_params.get('tipus_contracte')
        if tipus_contracte is not None:
            queryset = queryset.filter(tipus_contracte_id=tipus_contracte)
        
        duracio_min = self.request.query_params.get('duracio_min')
        if duracio_min is not None:
            queryset = queryset.filter(duracio_contracte__gte=duracio_min)
        
        duracio_max = self.request.query_params.get('duracio_max')
        if duracio_max is not None:
            queryset = queryset.filter(duracio_contracte__lte=duracio_max)
        
        data_inici = self.request.query_params.get('data_inici')
        if data_inici is not None:
            queryset = queryset.filter(data_inici__gte=data_inici)

        data_fi = self.request.query_params.get('data_fi')
        if data_fi is not None:
            queryset = queryset.filter(data_fi__lte=data_fi)

        return queryset



class LicitacionsPrivadesList(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]  # Specify TokenAuthentication for authentication

    def get_permissions(self):
        if self.request.method == 'POST':
            # Require authentication for the POST method
            return [permissions.IsAuthenticated()]
        else:
            # Allow unauthenticated access for the GET method
            return []

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LicitacioPrivadaPreviewSerializer
        elif self.request.method == 'POST':
            lloc_execucio = self.request.data.get('lloc_execucio')  # Assuming lloc_execucio is passed in the request data
            print(lloc_execucio)
            if lloc_execucio:
                # Check if the lloc_execucio exists in the database or create it
                localitzacio = get_lloc_execucio(lloc_execucio)
                #serializer.validated_data['lloc_execucio'] = localitzacio
            return LicitacioPrivadaDetailsSerializer
        else:
            # Return the default serializer class
            return self.serializer_class

    def get_queryset(self):
        queryset = LicitacioPrivada.objects.all()

        localitzacio = self.request.query_params.get('lloc_execucio')
        if localitzacio is not None:
            queryset = queryset.filter(lloc_execucio__nom__icontains=localitzacio)

        pressupost_min = self.request.query_params.get('pressupost_min')
        if pressupost_min is not None:
            queryset = queryset.filter(pressupost__gte=pressupost_min)
        
        pressupost_max = self.request.query_params.get('pressupost_max')
        if pressupost_max is not None:
            queryset = queryset.filter(pressupost__lte=pressupost_max)
        
        tipus_contracte = self.request.query_params.get('tipus_contracte')
        if tipus_contracte is not None:
            queryset = queryset.filter(tipus_contracte_id=tipus_contracte)
        
        duracio_min = self.request.query_params.get('duracio_min')
        if duracio_min is not None:
            queryset = queryset.filter(duracio_contracte__gte=duracio_min)
        
        duracio_max = self.request.query_params.get('duracio_max')
        if duracio_max is not None:
            queryset = queryset.filter(duracio_contracte__lte=duracio_max)
        
        data_inici = self.request.query_params.get('data_inici')
        if data_inici is not None:
            queryset = queryset.filter(data_inici__gte=data_inici)

        data_fi = self.request.query_params.get('data_fi')
        if data_fi is not None:
            queryset = queryset.filter(data_fi__lte=data_fi)

        return queryset
    
    def perform_create(self, serializer):
        licitacio = serializer.save(user=self.request.user)
        try:
            followers = Follow.objects.filter(following = self.request.user)
        except:
            print('No tiene followers')
        for f in followers:
            Notification.objects.create(
                            user = f.follower,
                            licitacio = licitacio,
                            mesage = 'Nueva publicación',
                            nom_licitacio = licitacio.denominacio
            )
        return Response(status.HTTP_201_CREATED)
            

   
class LicitacionsFavoritesList(generics.ListAPIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)
    serializer_class = LicitacioPreviewSerializer

    def get_queryset(self):
        user = self.request.user
        favorits = ListaFavorits.objects.filter(user=user).values_list('licitacio_id', flat=True)
        return Licitacio.objects.filter(id__in=favorits)

    
class LicitacionsSeguidesList(generics.ListAPIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)
    serializer_class = LicitacioPreviewSerializer

    def get_queryset(self):
        user = self.request.user
        seguint = ListaFavorits.objects.filter(user=user, notificacions = True).values_list('licitacio_id', flat=True)
        return Licitacio.objects.filter(id__in=seguint)


class LicitacionsApliedList(generics.ListAPIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)
    serializer_class = LicitacioPreviewSerializer

    def get_queryset(self):
        user = self.request.user
        seguint = Candidatura.objects.filter(user=user).values_list('licitacio_id', flat=True)
        return Licitacio.objects.filter(id__in=seguint)


class LicitacionsFollowingList(generics.ListAPIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)
    serializer_class = LicitacioPrivadaPreviewSerializer

    def get_queryset(self):
        user = self.request.user
        following = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
        return LicitacioPrivada.objects.filter(user__in=following)
    

class LicitacionsPreferencesList(generics.ListAPIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)
    serializer_class = LicitacioPreviewSerializer

    def get_queryset(self):
        user = self.request.user

        tp_preferences = PreferenceTipusContracte.objects.filter(user=user).values_list('tipus_contracte', flat=True)
        ambit_preferences = PreferenceAmbit.objects.filter(user=user).values_list('ambit', flat=True)
        lic_pub_ids = LicitacioPublica.objects.filter(ambit__in=ambit_preferences).values_list('licitacio_ptr_id', flat=True)
        pressupost_preferences = PreferencePressupost.objects.filter(user=user).first()
        tl_preferences = PreferenceTipusLicitacio.objects.filter(user=user).first()

        queryset = Licitacio.objects.none()

        if tl_preferences:
            if tl_preferences.privades:
                ids_privades = LicitacioPrivada.objects.all().values_list('licitacio_ptr_id', flat=True)
                queryset = queryset | Licitacio.objects.filter(id__in=ids_privades)
            
            if tl_preferences.publiques:
                ids_publiques = LicitacioPublica.objects.all().values_list('licitacio_ptr_id', flat=True)
                queryset = queryset | Licitacio.objects.filter(id__in=ids_publiques)

        if tp_preferences:
            queryset = queryset & Licitacio.objects.filter(tipus_contracte__in=tp_preferences)


        if pressupost_preferences:
            if pressupost_preferences.pressupost_min is not None and pressupost_preferences.pressupost_max is None:
                q = Q(pressupost__gte=pressupost_preferences.pressupost_min)
            elif pressupost_preferences.pressupost_min is None and pressupost_preferences.pressupost_max is not None:
                q = Q(pressupost__lte=pressupost_preferences.pressupost_max)
            elif pressupost_preferences.pressupost_min is not None and pressupost_preferences.pressupost_max is not None:
                q = Q(pressupost__gte=pressupost_preferences.pressupost_min, pressupost__lte=pressupost_preferences.pressupost_max)
            
            queryset = queryset & Licitacio.objects.filter(q)
        
        queryset = queryset | Licitacio.objects.filter(id__in=lic_pub_ids)

        return queryset


class LocalitzacionsInfo(generics.ListAPIView):
    serializer_class = LocalitzacioInfoSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Localitzacio.objects.all().order_by('nom')

        localitzacio = self.request.query_params.get('lloc_execucio')
        if localitzacio is not None:
            queryset = queryset.filter(nom__icontains=localitzacio)
        return queryset


class AmbitsInfo(generics.ListAPIView):
    serializer_class = AmbitInfoSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Ambit.objects.all().order_by('nom')

        ambit = self.request.query_params.get('ambit')
        if ambit is not None:
            queryset = queryset.filter(nom__icontains=ambit)
        return queryset


class DepartamentsInfo(generics.ListAPIView):
    serializer_class = DepartamentInfoSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Departament.objects.all().order_by('nom')

        departament = self.request.query_params.get('departament')
        if departament is not None:
            queryset = queryset.filter(nom__icontains=departament)
        return queryset
    

class OrgansInfo(generics.ListAPIView):
    serializer_class = OrganInfoSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Organ.objects.all().order_by('nom')

        organ = self.request.query_params.get('organ')
        if organ is not None:
            queryset = queryset.filter(nom__icontains=organ)
        return queryset


class TipusContracteInfo(generics.ListAPIView):
    serializer_class = TipusContracteInfoSerializer
    pagination_class = None
    
    def get_queryset(self):
        queryset = TipusContracte.objects.all().order_by('tipus_contracte')

        tipus_contracte = self.request.query_params.get('tipus_contracte')
        if tipus_contracte is not None:
            queryset = queryset.filter(Q(tipus_contracte__icontains=tipus_contracte) | Q(subtipus_contracte__icontains=tipus_contracte))
        return queryset


class Add_to_favorites(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)
    
    def post(self,request, pk):
        user = request.user
        licitacio = get_object_or_404(Licitacio, pk=pk)
        favorit = ListaFavorits.objects.filter(user=user, licitacio=licitacio).first()
        if favorit:
            licitacio.num_favorits = licitacio.num_favorits - 1
            licitacio.save()
            favorit.delete()
            response_data = {'licitacio': pk, 'user': user.email, 'action': 'deleted from favorites', 'success': True}
        else:
            if(licitacio.num_favorits == None):
                licitacio.num_favorits = 1
            else:
                licitacio.num_favorits = licitacio.num_favorits + 1
            licitacio.save()
            favorit = ListaFavorits(user=user, licitacio=licitacio)
            favorit.save()
            response_data = {'licitacio': pk, 'user': user.email, 'action': 'added to favorites', 'success': True}
        return JsonResponse(response_data)


class Seguir(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)
    
    def post(self,request, pk):
        user = request.user
        licitacio = get_object_or_404(Licitacio, pk=pk)
        seguir = ListaFavorits.objects.filter(user=user, licitacio=licitacio).first()
        if seguir:
            if seguir.notificacions == True:
                seguir.notificacions=False
                seguir.save()
                response_data = {'licitacio': pk, 'user': user.email, 'action': 'Deixant de seguir licitacio', 'success': True}
            else:
                seguir.notificacions=True
                seguir.save() 
                response_data = {'licitacio': pk, 'user': user.email, 'action': 'Seguint licitacio', 'success': True}
        else:
            response_data = {'licitacio': pk, 'user': user.email, 'action': 'First add it to favorites', 'success': False}
        
        return JsonResponse(response_data)



class VisualitzarCandidatura(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)
    
    def get(self,request, pk):
        try:
            candidatura = Candidatura.objects.get(id = pk)
            serializercand = CandidaturaSerializer(candidatura)
        except Candidatura.DoesNotExist:
            return Response({'error': 'La candidatura no existe'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializercand.data, status=status.HTTP_200_OK)


class Aply(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def post(self,request, pk):
        user = request.user
        motiu = request.data.get('motiu')
        print(motiu)
        licitacio = get_object_or_404(LicitacioPrivada, pk=pk)
        print('peta')
        aplied = Candidatura.objects.filter(user=user, licitacio=licitacio).first()
        if aplied:
            aplied.delete()
            licitacio.ofertes_rebudes = licitacio.ofertes_rebudes - 1
            licitacio.save()
        else:
            aplied = Candidatura(user=user, licitacio=licitacio, motiu=motiu)
            aplied.save()
            if(licitacio.ofertes_rebudes == None):
                licitacio.ofertes_rebudes = 1     
            else:
                licitacio.ofertes_rebudes = licitacio.ofertes_rebudes + 1
            licitacio.save()
            notification = Notification.objects.create(
                        user = licitacio.user,
                        licitacio = licitacio,
                        mesage = 'Usuario presentado',
                        nom_licitacio = licitacio.denominacio
                    )
            return Response(NotificationSerializer(notification).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_200_OK)


class AcceptAplicant(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def post(self,request):
        user = request.user
        candidatura_id = request.data.get('candidatura')
        candidatura = get_object_or_404(Candidatura, pk=candidatura_id)
        licitacio = get_object_or_404(LicitacioPrivada, pk=candidatura.licitacio)

        if user == licitacio.user:
            candidatures = Candidatura.objects.filter(licitacio=licitacio)
            candidatura.estat = 'Acceptada'
            candidatura.save()
            candidatures.exclude(id=candidatura_id).update(estat='Rebutjada')
            try:
                Notification.objects.create(
                    user = candidatura.user,
                    mesage = 'Candidatura aceptada',
                    licitacio = licitacio,
                    nom_licitacio = licitacio.denominacio
                )
            except:
                return Response({"error":"Error al generar la notificacion"})
            return Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class DeclineAplicant(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def post(self,request):
        user = request.user
        candidatura_id = request.data.get('candidatura')
        candidatura = get_object_or_404(Candidatura, pk=candidatura_id)
        licitacio = get_object_or_404(LicitacioPrivada, pk=candidatura.licitacio)

        if user == licitacio.user:
            candidatura.estat = 'Rebutjada'
            candidatura.save()
            try:
                Notification.objects.create(
                    user = candidatura.user,
                    mesage = 'Candidatura rechazada',
                    licitacio = licitacio,
                    nom_licitacio = licitacio.denominacio
                )
            except:
                return Response({"error":"Error al generar la notificacion"})
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class Estadistiques(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def get(self, request, pk):
        print("HE ENTRADO")
        try:
            licitacio = Licitacio.objects.get(id = pk)
        except Licitacio.DoesNotExist:
            print("No existe")
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EstadistiquesSerializer(licitacio)
        return Response(serializer.data, status.HTTP_200_OK)


class LicitacionsPrivadesUser(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def get(self,request):
        user = request.user
        try:
            licitacions = LicitacioPrivada.objects.filter(user = user)
        except LicitacioPrivada.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LicitacioPrivadaPreviewSerializer(licitacions, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class LicitacionsPrivadesUserAplicants(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def get(self,request):
        user = request.user
        try:
            licitacions = LicitacioPrivada.objects.filter(user = user).values_list('licitacio_ptr_id', flat=True)
        except LicitacioPrivada.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        candidatures = Candidatura.objects.filter(
            Q(licitacio_id__in=licitacions) & Q(estat="En procés")
        ).order_by('licitacio')
        serializer = CandidaturaSerializer(candidatures, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
