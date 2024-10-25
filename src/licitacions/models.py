from django.conf import settings
from django.db import models
from licitacions import choices

# Create your models here.

class Localitzacio(models.Model):
    nom = models.CharField(max_length=100, primary_key=True)
    longitud = models.DecimalField(max_digits=22, decimal_places=16, null=True)
    latitud = models.DecimalField(max_digits=22, decimal_places=16, null=True)

    def __str__(self):
        return self.nom


class Ambit(models.Model):
    codi = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=100, verbose_name="nom àmbit")

    def __str__(self):
        return self.nom


class Departament(models.Model):
    codi = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=100, verbose_name="nom departament")

    def __str__(self):
        return self.nom


class Organ(models.Model):
    codi = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=100, verbose_name="nom organ")

    def __str__(self):
        return self.nom


class TipusContracte(models.Model):
    tipus_contracte = models.CharField(max_length=50)
    subtipus_contracte = models.CharField(max_length=250)

    class Meta:
        unique_together = ('tipus_contracte', 'subtipus_contracte')

    def __str__(self):
        return self.tipus_contracte + ': ' + self.subtipus_contracte


class Licitacio(models.Model):
    denominacio = models.TextField(null=True)
    objecte_contracte = models.TextField(null=True)
    pressupost = models.DecimalField(decimal_places=2, max_digits=100, null=True)
    valor_estimat_contracte = models.DecimalField(decimal_places=2, max_digits=100, null=True)
    duracio_contracte = models.IntegerField(null=True)
    data_inici = models.DateField(null=True)
    data_fi = models.DateField(null=True)
    termini_presentacio_ofertes = models.DateTimeField(null=True)
    data_publicacio_anunci = models.DateTimeField(null=True)
    data_publicacio_adjudicacio = models.DateTimeField(null=True)
    import_adjudicacio_sense_iva = models.DecimalField(decimal_places=2, max_digits=100, null=True)
    import_adjudicacio_amb_iva = models.DecimalField(decimal_places=2, max_digits=100, null=True)
    ofertes_rebudes = models.IntegerField(default=0, null=True)
    resultat = models.CharField(max_length=50, null=True)
    data_adjudicacio_contracte = models.DateField(null=True)
    data_formalitzacio_contracte = models.DateField(null=True)
    lloc_execucio = models.ForeignKey(Localitzacio, to_field='nom', related_name="licitacio", null=True, on_delete=models.SET_NULL)
    tipus_contracte = models.ForeignKey(TipusContracte, to_field='id', related_name="licitacio", null=True, on_delete=models.SET_NULL)
    visualitzacions = models.IntegerField(null=True)
    num_favorits = models.IntegerField(null=True)

    def tipus_contracte_name(self):
        return TipusContracte.objects.filter(id=self.tipus_contracte).__str__


class LicitacioPublica(Licitacio):
    procediment = models.CharField(max_length=150, choices=choices.procediments, null=True)
    fase_publicacio = models.CharField(max_length=80, choices=choices.fase_publicacio, null=True)
    codi_cpv = models.CharField(max_length=200, null=True)
    enllaç = models.URLField(null=True)
    ambit = models.ForeignKey(Ambit, to_field='codi', related_name="licitacio_publica", null=True, on_delete=models.SET_NULL)
    departament = models.ForeignKey(Departament, to_field='codi', related_name="licitacio_publica", null=True, on_delete=models.SET_NULL)
    organ = models.ForeignKey(Organ, to_field='codi', related_name="licitacio_publica", null=True, on_delete=models.SET_NULL)


class LicitacioPrivada(Licitacio):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='licitacio_privada')


class ListaFavorits(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='favorits')
    licitacio = models.ForeignKey(Licitacio, on_delete=models.CASCADE, null=True, blank=True, related_name='favorits')
    notificacions = models.BooleanField(default=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'licitacio'], name='unique_favorits'
            )
        ]


class PreferenceTipusContracte(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="preference_tipus_contracte")
    tipus_contracte = models.ForeignKey(TipusContracte, to_field='id', related_name="preference_tipus_contracte", null=True, on_delete=models.CASCADE)    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'tipus_contracte'], name='unique_preference_tipus_contracte'
            )
        ]


class PreferenceAmbit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="preference_ambit")
    ambit = models.ForeignKey(Ambit, to_field='codi', related_name="preference_ambit", null=True, on_delete=models.CASCADE)    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'ambit'], name='unique_preference_ambit'
            )
        ]


class PreferencePressupost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preference_pressupost", primary_key=True)
    pressupost_min = models.DecimalField(decimal_places=2, max_digits=100, null=True)    
    pressupost_max = models.DecimalField(decimal_places=2, max_digits=100, null=True)


class PreferenceTipusLicitacio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preference_tipus_licitacio", primary_key=True)
    privades = models.BooleanField(default=False)
    publiques = models.BooleanField(default=False)


class Candidatura(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="candidatura", null=True, blank=True)
    licitacio = models.ForeignKey(LicitacioPrivada, on_delete=models.CASCADE, null=True, blank=True, related_name='candidatura')
    motiu = models.TextField(null=True)
    estat = models.TextField(max_length=150, choices=choices.estat_candidatura, null=True, default='En procés')
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'licitacio'], name='unique_candidatura'
            )
        ]
