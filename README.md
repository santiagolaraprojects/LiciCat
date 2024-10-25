# Back-end

## Com crear el Virutal Enviroment
Entra a l'arrel del projecte i executa:
  ```
  python -m venv .
  ```
Aixo creara el virtual enviorment el qual NO s'ha de posar al repositori git.

## Com obrir activar el Virutal Enviroment
  Entra a l'arrel del projecte i executa l'script Activate:
- Si s'utilitza PowerShell:
  ```
  .\Scripts\Activate.ps1
  ```
- Si s'utilitza Linux o Mac:
  ```
  source bin/activate
  ```

## Com instalar les llibreries:
Per actualitzar totes les llibreries de python, amb els Virutal Enviroment activat executa (es requereix python>=3.8):
```
python -m pip install -r requirements.txt
```

## Com instalar noves llibreries:
Per instalar una llibreria python instalarla utilitzant pip:
```
python -m pip install Django
```
A continuació actualitzar el fitxer requirements.txt
```
python -m pip freeze > requirements.txt
```

# Como entrar a la rama develop
Primero comprobar en que rama estmos:
```
git status 
```
Nos lo indicarà diciendo: On branch <branch_name>

Ejecutar el comando:
```
git checkout develop 
```
Tras ejectuarlo deberia cambiar a la rama develop, para asegurarse volver a ejecutar git status y 
asegurarnos de que la rama actual es develop.

# Como crear una nueva rama
Crear una rama local:
```
git checkout -b <branch_name>
```
# Como convertir la rama local a remota
```
git push develop <local_branch>
```
#Crear Django App
```
python manage.py startapp app_name
```
