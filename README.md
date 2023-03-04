## Online service for generating CSV-files with fake (dummy) data
## Site

http://korny4.pythonanywhere.com/ 


## Run  
Install requirements for this project
```
pip install -r requirementa.txt
```
Navigate to the project directory (where manage.py is located) and run
```
python manage.py makemigrations
python manage.py migrate
```
Create superuser for django admin panel
```
python manage.py createsuperuser
```
Run the project
```
python manage.py runserver
```
Run the redis for celery

```
docker-compose up -d
``` 

Run celery

```
celery -A csv_generating_service worker -l info 
```
