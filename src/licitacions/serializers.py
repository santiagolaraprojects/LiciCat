from rest_framework import serializers
from licitacions import models
from users.serializers import UserProfileSerializer
from .models import ListaFavorits
from users.models import CustomUser

class LicitacioPreviewSerializer(serializers.ModelSerializer):
    tipus_contracte = serializers.StringRelatedField(many=False)
    favorit = serializers.SerializerMethodField()
    notificacions = serializers.SerializerMethodField()
    candidatura = serializers.SerializerMethodField()
    estat_candidatura = serializers.SerializerMethodField()

    class Meta:
        model = models.Licitacio
        fields = ('id', 'lloc_execucio', 'pressupost', 'denominacio', 'tipus_contracte', 'data_inici', 'data_fi', 'favorit', 'notificacions', 'candidatura', 'estat_candidatura')
    
    def get_favorit(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                models.ListaFavorits.objects.get(user=user, licitacio=obj)
                return True
            except models.ListaFavorits.DoesNotExist:
                pass
        return False
    
    def get_notificacions(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                models.ListaFavorits.objects.get(user=user, licitacio=obj)
                return True
            except models.ListaFavorits.DoesNotExist:
                pass
        return False
    
    def get_candidatura(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                models.Candidatura.objects.get(user=user, licitacio=obj)
                return True
            except models.Candidatura.DoesNotExist:
                pass
        return False

    def get_estat_candidatura(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                candidatura = models.Candidatura.objects.get(user=user, licitacio=obj)
                return candidatura.estat
            except models.Candidatura.DoesNotExist:
                pass
        return "not aplied"

class LicitacioPublicaPreviewSerializer(serializers.ModelSerializer):
    tipus_contracte = serializers.StringRelatedField(many=False)
    favorit = serializers.SerializerMethodField()
    notificacions = serializers.SerializerMethodField()


    class Meta:
        model = models.LicitacioPublica
        fields = ('id', 'lloc_execucio', 'pressupost', 'denominacio', 'tipus_contracte', 'favorit', 'notificacions')
    
    def get_favorit(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                models.ListaFavorits.objects.get(user=user, licitacio=obj)
                return True
            except models.ListaFavorits.DoesNotExist:
                pass
        return False
    
    def get_notificacions(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                models.ListaFavorits.objects.get(user=user, licitacio=obj, notificacions = True)
                return True
            except models.ListaFavorits.DoesNotExist:
                pass
        return False
    

class LicitacioPublicaDetailsSerializer(serializers.ModelSerializer):
    tipus_contracte = serializers.StringRelatedField(many=False)
    ambit = serializers.StringRelatedField(many=False)
    departament = serializers.StringRelatedField(many=False)
    organ = serializers.StringRelatedField(many=False)
    favorit = serializers.SerializerMethodField()
    notificacions = serializers.SerializerMethodField()

    class Meta:
        model = models.LicitacioPublica
        fields = '__all__'
    
    def get_favorit(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                models.ListaFavorits.objects.get(user=user, licitacio=obj)
                return True
            except models.ListaFavorits.DoesNotExist:
                pass
        return False
    
    def get_notificacions(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                models.ListaFavorits.objects.get(user=user, licitacio=obj, notificacions = True)
                return True
            except models.ListaFavorits.DoesNotExist:
                pass
        return False

    
class LicitacioPrivadaPreviewSerializer(serializers.ModelSerializer):
    favorit = serializers.SerializerMethodField()
    notificacions = serializers.SerializerMethodField()
    candidatura = serializers.SerializerMethodField()
    estat_candidatura = serializers.SerializerMethodField()


    class Meta:
        model = models.LicitacioPrivada
        fields = ('id', 'lloc_execucio', 'pressupost', 'denominacio', 'tipus_contracte', 'favorit', 'notificacions', 'candidatura', 'estat_candidatura')
    
    def get_favorit(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                models.ListaFavorits.objects.get(user=user, licitacio=obj)
                return True
            except models.ListaFavorits.DoesNotExist:
                pass
        return False
    
    def get_notificacions(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                models.ListaFavorits.objects.get(user=user, licitacio=obj, notificacions = True)
                return True
            except models.ListaFavorits.DoesNotExist:
                pass
        return False
    
    def get_candidatura(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                models.Candidatura.objects.get(user=user, licitacio=obj)
                return True
            except models.Candidatura.DoesNotExist:
                pass
        return False
    
    def get_estat_candidatura(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                candidatura = models.Candidatura.objects.get(user=user, licitacio=obj)
                return candidatura.estat
            except models.Candidatura.DoesNotExist:
                pass
        return "not aplied"
    

class LicitacioPrivadaDetailsSerializer(serializers.ModelSerializer):
    favorit = serializers.SerializerMethodField()
    notificacions = serializers.SerializerMethodField()
    candidatura = serializers.SerializerMethodField()
    estat_candidatura = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = models.LicitacioPrivada
        fields = '__all__'
    
    
    def get_favorit(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                models.ListaFavorits.objects.get(user=user, licitacio=obj)
                return True
            except models.ListaFavorits.DoesNotExist:
                pass
        return False
    
    def get_notificacions(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                models.ListaFavorits.objects.get(user=user, licitacio=obj, notificacions = True)
                return True
            except models.ListaFavorits.DoesNotExist:
                pass
        return False
    
    def get_candidatura(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                models.Candidatura.objects.get(user=user, licitacio=obj)
                return True
            except models.Candidatura.DoesNotExist:
                pass
        return False

    def get_estat_candidatura(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                candidatura = models.Candidatura.objects.get(user=user, licitacio=obj)
                return candidatura.estat
            except models.Candidatura.DoesNotExist:
                pass
        return "not aplied"
    
    def get_username(self, obj):
        return obj.user.username

class LocalitzacioInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Localitzacio
        fields = ('nom',)


class AmbitInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ambit
        fields = '__all__'


class DepartamentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Departament
        fields = '__all__'


class OrganInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organ
        fields = '__all__'


class TipusContracteInfoSerializer(serializers.ModelSerializer):
    contracte_str = serializers.SerializerMethodField()
    class Meta:
        model = models.TipusContracte
        fields = ('id', 'contracte_str')
    
    def get_contracte_str(self, obj):
        return str(obj)


class ListaFavoritsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaFavorits
        fields = '__all__'


class CandidaturaSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = models.Candidatura
        fields = '__all__'

class EstadistiquesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Licitacio
        fields = ('id', 'ofertes_rebudes', 'visualitzacions', 'num_favorits')