Pasos para ajustar la app 
  python -m venv venv
  pip install django
1 activar el entorno virtual 
  venv\Scripts\activate
2 entrar a proyecto_reciclaje
  cd proyecto_reciclaje
3 comentar custouser en models
4 generar las migraciones
  python manage.py makemigrations
5 en consola o en cmd 
  python manage.py migrate 
6 descomentar customuser en models
7 generar las migraciones
  python manage.py makemigrations
8 en consola o en cmd 
  python manage.py migrate 
9 obviar las migraciones 
  python manage.py migrate --fake
10 hashear las contraseña con el script
  python manage.py hash_passwords
11 correr el servidor 
  python manage.py runserver