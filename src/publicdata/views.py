from django.shortcuts import render
from django.db import transaction
from django.http import JsonResponse
from licitacions.models import Localitzacio, Ambit, Departament, Organ, TipusContracte, LicitacioPublica, LicitacioPrivada, ListaFavorits
from decimal import Decimal, getcontext
import requests
import json
import csv
from datetime import datetime, date
from users.views import Notification


def test():
# Objeto JSON de ejemplo
    PARAMS = 'procediment, fase_publicacio, denominacio, objecte_contracte, pressupost_licitacio, valor_estimat_contracte, duracio_contracte, termini_presentacio_ofertes, data_publicacio_anunci, data_publicacio_adjudicacio, codi_cpv, import_adjudicacio_sense, import_adjudicacio_amb_iva, ofertes_rebudes, resultat, data_adjudicacio_contracte, data_formalitzacio_contracte, enllac_publicacio, lloc_execucio, codi_ambit, nom_ambit, codi_departament_ens, nom_departament_ens, codi_organ, nom_organ, tipus_contracte, subtipus_contracte'
    num_rows = '200000'
    base_url = 'https://analisi.transparenciacatalunya.cat/resource/a23c-d6vp.json?$query=SELECT ' + PARAMS + ' LIMIT ' + num_rows
    response_API = requests.get(base_url)
    data = response_API.text
    parse_json = json.loads(data)

    # Nombre del archivo .json
    nombre_archivo = "/home/santi/Documents/PES/ejemplo.json"

    # Crear el archivo .json y guardar el objeto JSON
    with open(nombre_archivo, "w") as archivo:
        json.dump(parse_json, archivo)

    print(f"Archivo {nombre_archivo} creado exitosamente con el objeto JSON.")

def get_data():
    PARAMS = 'procediment, fase_publicacio, denominacio, objecte_contracte, pressupost_licitacio, valor_estimat_contracte, duracio_contracte, termini_presentacio_ofertes, data_publicacio_anunci, data_publicacio_adjudicacio, codi_cpv, import_adjudicacio_sense, import_adjudicacio_amb_iva, ofertes_rebudes, resultat, data_adjudicacio_contracte, data_formalitzacio_contracte, enllac_publicacio, lloc_execucio, codi_ambit, nom_ambit, codi_departament_ens, nom_departament_ens, codi_organ, nom_organ, tipus_contracte, subtipus_contracte'
    num_rows = '1000'
    base_url = 'https://analisi.transparenciacatalunya.cat/resource/a23c-d6vp.json?$query=SELECT ' + PARAMS + ' LIMIT ' + num_rows
    response_API = requests.get(base_url)
    data = response_API.text
    parse_json = json.loads(data)
    print('Hay ' + str(len(parse_json)) + 'filas')

    fecha_formato = '%d/%m/%Y'


    with transaction.atomic():
        for licitacio in parse_json:
            procediment = licitacio.get('procediment')
            fase_publicacio = licitacio.get('fase_publicacio')
            denominacio = licitacio.get('denominacio')
            objecte_contracte = licitacio.get('objecte_contracte')

            pressupost_licitacio = licitacio.get('pressupost_licitacio')
            if(pressupost_licitacio is None):
                pressupost_licitacio = 0.00
            else: 
                pressupost_licitacio = Decimal(pressupost_licitacio)

            valor_estimat_contracte = licitacio.get('valor_estimat_contracte')
            if(valor_estimat_contracte is None):
                valor_estimat_contracte = 0.00
            else: 
                valor_estimat_contracte = Decimal(valor_estimat_contracte)

                
            duracio_contracte = licitacio.get('duracio_contracte')
            data_inici = None
            data_fi = None

            #Tiene data inici i data fi
            if(duracio_contracte != None):
                fechas = duracio_contracte.split()
                if(len(fechas[0]) == 10):

                    data_inici = datetime.strptime(fechas[0], fecha_formato).date()
                    data_fi = datetime.strptime(fechas[2], fecha_formato).date()

                    duracio_contracte = (data_fi - data_inici).days
                else:
                    duracio_contracte = int(fechas[0])*365 + int(fechas[2])*30 + int(fechas[4])

            termini_presentacio_ofertes = licitacio.get('termini_presentacio_ofertes')
            if(termini_presentacio_ofertes is not None):
                resultsplit = termini_presentacio_ofertes.split('T')
                termini_presentacio_ofertes = str(resultsplit[0])

            data_publicacio_anunci = licitacio.get('data_publicacio_anunci')
            if(data_publicacio_anunci is not None):
                resultsplit = data_publicacio_anunci.split('T')
                data_publicacio_anunci = str(resultsplit[0])

            data_publicacio_adjudicacio = licitacio.get('data_publicacio_adjudicacio')
            if(data_publicacio_adjudicacio is not None):           
                resultsplit = data_publicacio_adjudicacio.split('T')
                data_publicacio_adjudicacio = str(resultsplit[0])

            codi_cpv = licitacio.get('codi_cpv')
            if(codi_cpv is not None):
                codi_cpv = str(codi_cpv)

            import_adjudicacio_sense_iva = licitacio.get('import_adjudicacio_sense')
            if(import_adjudicacio_sense_iva is None):
                import_adjudicacio_sense_iva = 0.00
            else:
                import_adjudicacio_sense_iva = Decimal(import_adjudicacio_sense_iva)

            
            import_adjudicacio_amb_iva = licitacio.get('import_adjudicacio_amb_iva')
            if(import_adjudicacio_amb_iva is None):
                import_adjudicacio_amb_iva = 0.00
            else:
                import_adjudicacio_amb_iva = Decimal(import_adjudicacio_amb_iva)

            

            ofertes_rebudes = licitacio.get('ofertes_rebudes')
            if(ofertes_rebudes is not None):
                ofertes_rebudes = int(ofertes_rebudes)

            resultat = licitacio.get('resultat')

            data_adjudicacio_contracte = licitacio.get('data_adjudicacio_contracte')
            if(data_adjudicacio_contracte is not None):
                resultsplit = data_adjudicacio_contracte.split('T')
                data_adjudicacio_contracte = str(resultsplit[0])

            
            data_formalitzacio_contracte = licitacio.get('data_formalitzacio_contracte')
            if(data_formalitzacio_contracte is not None):
                resultsplit = data_formalitzacio_contracte.split('T')
                data_formalitzacio_contracte = str(resultsplit[0])

            new_enllaç = licitacio.get('enllac_publicacio')

            lloc_execucio = get_lloc_execucio(licitacio.get('lloc_execucio'))

            ambit = get_ambit(licitacio.get('nom_ambit'), licitacio.get('codi_ambit'))

            departament = get_departament(licitacio.get('nom_departament_ens'), licitacio.get('codi_departament_ens'))
    
            organ = get_organ(licitacio.get('nom_organ'), licitacio.get('codi_organ'))

            tipus_contracte = get_tipus_contracte(licitacio.get('tipus_contracte'), licitacio.get('subtipus_contracte'))

            try:
                db_licitacio = LicitacioPublica.objects.get(enllaç=new_enllaç)
                db_licitacio.procediment = procediment
                db_licitacio.fase_publicacio = fase_publicacio
                db_licitacio.objecte_contracte = objecte_contracte
                db_licitacio.pressupost = pressupost_licitacio
                db_licitacio.valor_estimat_contracte = valor_estimat_contracte
                db_licitacio.duracio_contracte = duracio_contracte
                db_licitacio.termini_presentacio_ofertes = termini_presentacio_ofertes
                db_licitacio.data_publicacio_anunci = data_publicacio_anunci
                db_licitacio.data_publicacio_adjudicacio = data_publicacio_adjudicacio
                db_licitacio.codi_cpv = codi_cpv
                db_licitacio.import_adjudicacio_sense_iva = import_adjudicacio_sense_iva
                db_licitacio.import_adjudicacio_amb_iva = import_adjudicacio_amb_iva
                db_licitacio.ofertes_rebudes = ofertes_rebudes
                db_licitacio.resultat = resultat
                db_licitacio.data_adjudicacio_contracte = data_adjudicacio_contracte
                db_licitacio.data_formalitzacio_contracte = data_formalitzacio_contracte
                db_licitacio.enllaç = new_enllaç
                db_licitacio.lloc_execucio = lloc_execucio
                db_licitacio.ambit = ambit
                db_licitacio.departament = departament
                db_licitacio.organ = organ
                db_licitacio.tipus_contracte = tipus_contracte
                db_licitacio.data_inici = data_inici
                db_licitacio.data_fi = data_fi
                db_licitacio.save()

                licitacioFollowed = (ListaFavorits.objects.filter(licitacio = db_licitacio))

                for l in licitacioFollowed:
                    if(l.notificacions):
                        Notification.objects.create(
                            user = l.user,
                            licitacio = l.licitacio,
                            mesage = 'Licitacion modificada',
                            nom_licitacio = l.licitacio.denominacio
                        )

            except LicitacioPublica.DoesNotExist:
                LicitacioPublica.objects.create(procediment = procediment,
                                fase_publicacio = fase_publicacio,
                                denominacio = denominacio,
                                objecte_contracte = objecte_contracte,
                                pressupost = pressupost_licitacio,
                                valor_estimat_contracte = valor_estimat_contracte,
                                duracio_contracte = duracio_contracte,
                                termini_presentacio_ofertes = termini_presentacio_ofertes,
                                data_publicacio_anunci = data_publicacio_anunci,
                                data_publicacio_adjudicacio = data_publicacio_adjudicacio,
                                codi_cpv = codi_cpv,
                                import_adjudicacio_sense_iva = import_adjudicacio_sense_iva,
                                import_adjudicacio_amb_iva = import_adjudicacio_amb_iva,
                                ofertes_rebudes = ofertes_rebudes,
                                resultat = resultat,
                                data_adjudicacio_contracte = data_adjudicacio_contracte,
                                data_formalitzacio_contracte = data_formalitzacio_contracte,
                                enllaç = new_enllaç,
                                lloc_execucio = lloc_execucio,
                                ambit = ambit, 
                                departament = departament, 
                                organ = organ,
                                tipus_contracte = tipus_contracte,
                                data_inici = data_inici,
                                data_fi = data_fi
                                )
            
           # if(exists):
                #print('ya existe')

    return JsonResponse(data, safe=False)

def create_db_from_csv(request):
    with open('/home/santi/Downloads/Contractaci__p_blica_a_Catalunya__licitacions_i_adjudicacions_en_curs.csv') as f:
        
        reader = csv.reader(f)
        next(reader)
        for row in reader:

            #Modificamos todas las fechas al formato correcto de DateTime 
            print('/////////////////////////////////////////////////////////////////////////////////////////////')
            data_publicacio_anunci = None
            if(row[25] != ''):
                print(len(row[25]))
                if(len(row[25]) > 10):
                    data_publicacio_anunci = datetime.strptime(row[25], '%d/%m/%Y %I:%M:%S %p')
                    data_publicacio_anunci = data_publicacio_anunci.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    data_publicacio_anunci = datetime.strptime(row[25], '%d/%m/%Y')
                    data_publicacio_anunci = datetime.combine(data_publicacio_anunci.date(), datetime.min.time())
            else:
                data_publicacio_anunci = None
            
            print('data_publicacio_anunci: ' )
            print(data_publicacio_anunci)

            data_publicacio_adjudicacio = None
            print(len(row[26]))
            if(row[26] != ''):
                if(len(row[26]) > 10):
                    data_publicacio_adjudicacio = datetime.strptime(row[26], '%d/%m/%Y %I:%M:%S %p')
                    data_publicacio_adjudicacio = data_publicacio_adjudicacio.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    data_publicacio_adjudicacio = datetime.strptime(row[26], '%d/%m/%Y')
                    data_publicacio_adjudicacio = datetime.combine(data_publicacio_adjudicacio.date(), datetime.min.time())
            else:
                data_publicacio_adjudicacio = None

            print('data_publicacio_adjudicacio: ' )
            print(data_publicacio_adjudicacio)

            data_adjudicacio_contracte = None
            if(row[41] != ''):
                print(len(row[41]))
                if(len(row[41]) > 10):
                    data_adjudicacio_contracte = datetime.strptime(row[41], '%d/%m/%Y %I:%M:%S %p')
                    data_adjudicacio_contracte = data_adjudicacio_contracte.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    data_adjudicacio_contracte = datetime.strptime(row[41], '%d/%m/%Y')
                    data_adjudicacio_contracte = datetime.combine(data_adjudicacio_contracte.date(), datetime.min.time())
            else:
                data_adjudicacio_contracte = None

            print('data_adjudicacio_contracte: ')
            print(data_adjudicacio_contracte)

            data_formalitzacio_contracte = None
            if(row[42] != ''):
                if(len(row[42]) > 10):
                    data_formalitzacio_contracte = datetime.strptime(row[42], '%d/%m/%Y %I:%M:%S %p')
                    data_formalitzacio_contracte = data_formalitzacio_contracte.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    data_formalitzacio_contracte = datetime.strptime(row[42], '%d/%m/%Y')
                    data_formalitzacio_contracte = datetime.combine(data_formalitzacio_contracte.date(), datetime.min.time())
                    data_formalitzacio_contracte = data_formalitzacio_contracte.replace(hour=0, minute=0, second=0)
            else:
                print('Alomejor ha petado')
                data_formalitzacio_contracte = None            

            print('data_formalitzacio_contracte: ')
            print(data_formalitzacio_contracte)

            termini_presentacio_ofertes = None
            if(row[22] != ''):
                print(len(row[22]))
                if(len(row[22]) > 10):
                    termini_presentacio_ofertes = datetime.strptime(row[22], '%d/%m/%Y %I:%M:%S %p')
                    termini_presentacio_ofertes = termini_presentacio_ofertes.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    termini_presentacio_ofertes = datetime.strptime(row[22], '%d/%m/%Y')
                    termini_presentacio_ofertes = datetime.combine(termini_presentacio_ofertes.date(), datetime.min.time())
            else:
                termini_presentacio_ofertes = None

            print('termini_presentacio_ofertes: ')
            print(termini_presentacio_ofertes)
            print('/////////////////////////////////////////////////////////////////////////////////////////////')

            #Modificamos los numeros decimales para que sean aceptados por Django
            pressupost = row[17]
            if(pressupost == ''):
                pressupost = None

            valor_estimat_contracte = row[18]
            if(valor_estimat_contracte == ''):
                valor_estimat_contracte = None

            import_adjudicacio_sense_iva = row[35]
            if(import_adjudicacio_sense_iva == ''):
                import_adjudicacio_sense_iva = None

            import_adjudicacio_amb_iva = row[36]
            if(import_adjudicacio_amb_iva == ''):
                import_adjudicacio_amb_iva = None

            ofertes_rebudes = row[37]
            if row[37].isdigit():
                ofertes_rebudes = int(row[37])
            else:
                ofertes_rebudes = None


            codi_cpv = None
            if(row[31] != ''):
                codi_cpv = row[31]

            print(row[13])    
            print(row[14])    
            print(row[15])    
            print(row[16])
            if(pressupost is None):
                print('None')    
            else:
                print(pressupost)
            if(valor_estimat_contracte is None):
                print('None')
            else:
                print(valor_estimat_contracte)    
            print(row[21])
            if(termini_presentacio_ofertes is None):
                print('None')
            else:    
                print(termini_presentacio_ofertes)
            if(data_publicacio_anunci is None):    
                print('None')    
            else:
                print(data_publicacio_anunci)
            if(data_publicacio_adjudicacio is None):
                print('None')
            else:
                print(data_publicacio_adjudicacio)    
            print(row[31])
            if(import_adjudicacio_sense_iva is None):
                print('None')
            else:    
                print(import_adjudicacio_sense_iva)    
            if(import_adjudicacio_amb_iva is None):
                print('None')
            else:
                print(import_adjudicacio_amb_iva)
            if(ofertes_rebudes is None):
                print('None')
            else:    
                print(ofertes_rebudes)    
            print(row[38])
            if(data_adjudicacio_contracte is None):    
                print('None')
            else:
                print(data_adjudicacio_contracte)  
            if(data_formalitzacio_contracte is None):
                print('None')
            else:  
                print(data_formalitzacio_contracte)    
            print(row[39])
        

            LicitacioPublica.objects.create(
                procediment = row[13],
                fase_publicacio = row[14],
                denominacio = row[15],
                objecte_contracte = row[16],
                pressupost = pressupost,
                valor_estimat_contracte = valor_estimat_contracte,
                duracio_contracte = row[21],
                termini_presentacio_ofertes = termini_presentacio_ofertes,
                data_publicacio_anunci = data_publicacio_anunci,
                data_publicacio_adjudicacio = data_publicacio_adjudicacio,
                codi_cpv = codi_cpv,
                import_adjudicacio_sense_iva = import_adjudicacio_sense_iva,
                import_adjudicacio_amb_iva = import_adjudicacio_amb_iva,
                ofertes_rebudes = ofertes_rebudes,
                resultat = row[38],
                data_adjudicacio_contracte = data_adjudicacio_contracte,
                data_formalitzacio_contracte = data_formalitzacio_contracte,
                enllaç = row[39],
                lloc_execucio = get_lloc_execucio(row[20]),
                ambit = get_ambit(row[1], row[0]), 
                departament = get_departament(row[3], row[2]), 
                organ = get_organ(row[5], row[4]),
                tipus_contracte = get_tipus_contracte(row[11], row[12])
                ) 




def delete_all_licitacions_publicas(request):
    LicitacioPublica.objects.all().delete()
    return render(request, 'ok.html')


def get_lloc_execucio(lloc_execucio):
    try:
        obj = Localitzacio.objects.get(nom=lloc_execucio)
        return obj
    except Localitzacio.DoesNotExist:
        url = "https://us-central1-discovery-f510f.cloudfunctions.net/getCityCoordinates"
        params = {"city": lloc_execucio}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            longitude = data.get("longitude", 0.0)
            latitude = data.get("latitude", 0.0)
            obj = Localitzacio(nom=lloc_execucio, longitud=Decimal(longitude), latitud=Decimal(latitude))
            obj.save()
            return obj
        else:
            # Handle the case when the request fails or returns an error
            # You can raise an exception or return a default value
            return None

def get_ambit(nom, codi):
    try:
        obj = Ambit.objects.get(codi = codi, nom = nom)
        return obj
    except Ambit.DoesNotExist:
        obj = Ambit(codi = codi, nom = nom)
        obj.save()
        return obj
    
def get_departament(nom, codi):
    try:
        obj = Departament.objects.get(codi = codi, nom = nom)
        return obj
    except Departament.DoesNotExist:
        obj = Departament(codi = codi, nom = nom)
        obj.save()
        return obj
    
def get_organ(nom, codi):
    try:
        obj = Organ.objects.get(codi = codi, nom = nom)
        return obj
    except Organ.DoesNotExist:
        obj = Organ(codi = codi, nom = nom)
        obj.save()
        return obj

def get_tipus_contracte(tipus_contracte, subtipus_contracte):
    if(tipus_contracte is None):
        tipus_contracte = 'No existent'
    if(subtipus_contracte is None):
        subtipus_contracte = 'No existent'
    try:
        obj = TipusContracte.objects.get(tipus_contracte = tipus_contracte, subtipus_contracte = subtipus_contracte)
        return obj
    except TipusContracte.DoesNotExist:
        obj = TipusContracte(tipus_contracte = tipus_contracte, subtipus_contracte = subtipus_contracte)
        obj.save()
        return obj
    
